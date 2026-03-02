#services/notification_service.py
from fastapi import HTTPException
from psycopg2.extras import Json
from backend.database.repository import Repository
from backend.database.schemas import NotificationCreate
from backend.services.notification_normalizer import normalize_event
from datetime import timedelta
from uuid import UUID
from datetime import datetime
import json

class NotificationService:

    def __init__(self, conn):
        self.conn = conn
        self.repo = Repository(conn)
    
    #regra de disparo

    def should_notify(self, notification: NotificationCreate) -> bool:
        # 1. Nunca duplicar o mesmo evento
        if self.repo.fetch_one(
            "notificacoes",
            {"event_id": notification.event_id}
        ):
            return False

        # 2. Tipos que sempre notificam
        if notification.type in {"ERROR", "SUCCESS"}:
            return True

        # 3. Evitar repetir mesmo estado (severity)
        last = self.repo.fetch_one_raw(
            """
            SELECT *
            FROM app_core.notificacoes
            WHERE type = %s
              AND reference->>'id' = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (notification.type, str(notification.reference["id"]))
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
                  AND created_at > now() - %s
                """,
                (notification.type, str(notification.reference["id"]), cooldown)
            )

            if recent:
                return False

        return True
    
    def processar_evento(self, event_id: int, user_id: UUID):

        evento = self.repo.fetch_one_raw(
            """
            SELECT *
            FROM app_core.notificacoes_eventos
            WHERE id = %s AND user_id = %s
            """,
            (event_id, str(user_id))
        )

        

        if isinstance(evento.get("reference"), str):
            evento["reference"] = json.loads(evento["reference"])

        if isinstance(evento.get("context"), str):
            evento["context"] = json.loads(evento["context"])

        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        self._enrich_reference(evento)

        notificacao = normalize_event(evento)

        if not notificacao:
            return None

        if not self.should_notify(notificacao):
            return None

        data = notificacao.dict()
        data["reference"] = Json(data["reference"])

        self.repo.insert("app_core.notificacoes", data)
        self.conn.commit()

        return {"message": "Notificação criada"}



    def criar_notificacao(self, notificacao: NotificationCreate):
        data = notificacao.dict()

        data["reference"] = Json(data["reference"])

        ok = self.repo.insert(
            "app_core.notificacoes",
            data
        )

        if not ok:
            raise HTTPException(status_code=400, detail="Erro ao registrar notificacao.")

        self.repo.commit()
        return {"message": "Notificacao registrada com sucesso"}
    

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
        ref = evento.get("reference", {})
        ref_type = ref.get("type")

        if ref_type == "PRODUCT":
            ref["nome"] = self.produto_service.get_nome_produto(ref["id"])

        # futuros tipos aqui
