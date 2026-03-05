#services/notification_service.py
from fastapi import HTTPException
from psycopg2.extras import Json
from backend.database.repository import Repository
from backend.database.schemas import NotificationCreate
from backend.services.notification_normalizer import normalize_event
from backend.services.produto_service import ProdutoService
from datetime import timedelta
from uuid import UUID
from datetime import datetime
import json
from datetime import timedelta

COOLDOWN = {
    "RUPTURE": timedelta(minutes=10),
    "LOW_STOCK": timedelta(minutes=5),
}

class NotificationService:
    def __init__(self, conn):
        self.conn = conn
        self.repo = Repository(conn)
        self.produto_service = ProdutoService(conn)
    
    #regra de disparo

    def should_notify(self, notification: NotificationCreate) -> bool:

        print("CHECANDO EVENTO:", notification.event_id, notification.user_id)
        # 1. Nunca duplicar o mesmo evento para o mesmo usuário
        if self.repo.fetch_one(
            "app_core.notificacoes",
            conditions={
                "event_id": notification.event_id,
                "user_id": str(notification.user_id)
            }
        ):
            return False

        ref = notification.reference

        # Segurança defensiva
        if not ref or not getattr(ref, "id", None):
            return False

        ref_id = str(ref.id)

        # 3. Evitar repetir mesmo estado (severity)
        last = self.repo.fetch_one_raw(
            """
            SELECT *
            FROM app_core.notificacoes
            WHERE type = %s
            AND reference->>'id' = %s
            AND user_id = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (notification.type, ref_id, str(notification.user_id))
        )

        if last and last["severity"] == notification.severity:
            return False

        # 4. Cooldown
        cooldown = COOLDOWN.get(notification.type)
        if cooldown:
            recent = self.repo.fetch_one_raw(
                """
                SELECT 1
                FROM app_core.notificacoes
                WHERE type = %s
                AND reference->>'id' = %s
                AND user_id = %s
                AND created_at > now() - %s
                """,
                (notification.type, ref_id, str(notification.user_id), cooldown)
            )

            if recent:
                return False

        print("PASSOU NA REGRA")
        return True
    
    def processar_evento_para_todos(self, event_id: int):
        
        evento = self.repo.fetch_one_raw(
            """
            SELECT *
            FROM app_core.notificacoes_eventos
            WHERE id = %s
            """,
            (event_id,)
        )

        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        self._enrich_reference(evento)

        notificacao_base = normalize_event(evento)

        if not notificacao_base:
            return None

        # Busca todos usuários ativos
        usuarios = self._buscar_usuarios_para_evento()
        print("USUARIOS ENCONTRADOS:", usuarios)

        for usuario in usuarios:
            
            notificacao = notificacao_base.copy()
            notificacao.user_id = usuario["id"]

            print("PROCESSANDO USER:", usuario["id"])

            if not self.should_notify(notificacao):
                continue

            data = notificacao.dict()
            data["reference"] = Json(data["reference"])
            data["user_id"] = str(usuario["id"])

            self.repo.insert("app_core.notificacoes", data)

        self.conn.commit()

        return {"message": "Notificações criadas para todos usuários ativos"}



    def criar_notificacao(self, notificacao: NotificationCreate):
        data = notificacao.dict()
        data["reference"] = Json(data["reference"])

        self.repo.insert("app_core.notificacoes", data)
        self.conn.commit()
        return {"message": "Notificação criada"}
    

    def listar_notificacoes(
        self,
        user_id: UUID,
        read: bool | None,
        limit: int,
        cursor: str | None
    ):
        params = [str(user_id)]
        where = ["user_id = %s"]

        if read is not None:
            where.append("read = %s")
            params.append(read)

        if cursor:
            where.append("created_at < %s")
            params.append(datetime.fromisoformat(cursor))

        where_sql = "WHERE " + " AND ".join(where)

        sql = f"""
            SELECT *
            FROM app_core.notificacoes
            {where_sql}
            ORDER BY created_at DESC
            LIMIT %s
        """

        params.append(limit)

        self.repo.cursor.execute(sql, params)
        return self.repo.cursor.fetchall()
    

    def buscar_por_id(self, notification_id: int, user_id: UUID):
        notificacao = self.repo.fetch_one_raw(
            """
            SELECT *
            FROM app_core.notificacoes
            WHERE id = %s AND user_id = %s
            """,
            (notification_id, str(user_id))
        )

        if not notificacao:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")

        return notificacao
    
    def marcar_como_lida(self, notification_id: int, user_id: UUID):
        rows = self.repo.cursor.execute(
            """
            UPDATE app_core.notificacoes
            SET read = true
            WHERE id = %s AND user_id = %s
            """,
            (notification_id, str(user_id))
        )

        self.conn.commit()

        if self.repo.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")

        return {"message": "Notificação marcada como lida"}

    def _enrich_reference(self, evento: dict):
        ref = evento.get("reference")

        # Se não há referência, não há nada para enriquecer
        if not ref:
            return

        # Se vier como string (dependendo do cursor), normaliza
        if isinstance(ref, str):
            try:
                import json
                ref = json.loads(ref)
                evento["reference"] = ref
            except Exception:
                return

        # Segurança final
        if not isinstance(ref, dict):
            return

        ref_type = ref.get("type")

        if ref_type == "PRODUCT":
            ref["nome"] = self.produto_service.get_nome_produto(ref["id"])

    def _buscar_usuarios_para_evento(self):
        return self.repo.execute_query("""
            SELECT id
            FROM app_core.usuarios
            WHERE ativo = true
            AND papel = 'gestor'
        """)