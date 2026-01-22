#services/notification_service.py
from fastapi import HTTPException
from psycopg2.extras import Json
from backend.database.repository import Repository
from backend.database.schemas import NotificationCreate
from backend.services.notification_normalizer import normalize_event
from datetime import timedelta

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
        last = self.repo.fetch_one(
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
            recent = self.repo.fetch_one(
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
    
    def processar_evento(self, event_id: int):

        evento = self.repo.fetch_one(
            "notificacoes_eventos",
            "id",
            event_id
        )

        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        self._enrich_reference(evento)

        notificacao = normalize_event(evento)

        if not notificacao:
            return None  # evento não gera notificação

        if not self.should_notify(notificacao):
            return None

        data = notificacao.dict()
        data["reference"] = Json(data["reference"])

        created = self.repo.insert(
            "app_core.notificacoes",
            data
        )

        self.conn.commit()
        return created



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
        read: bool | None,
        limit: int,
        cursor: str | None
    ):
        params = []
        where = []

        if read is not None:
            where.append("read = %s")
            params.append(read)

        if cursor:
            where.append("created_at < %s")
            params.append(datetime.fromisoformat(cursor))

        where_sql = "WHERE " + " AND ".join(where) if where else ""

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
    

    def buscar_por_id(self, notification_id: int):
        notificacao = self.repo.fetch_one(
            "notificacoes",
            "id",
            notification_id
        )
        if not notificacao:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
        return notificacao

    def marcar_como_lida(self, notification_id: int):
        rows = self.repo.update(
            "app_core.notificacoes",
            "id",
            notification_id,
            {"read": True}
        )

        if rows == 0:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")

        return {"message": "Notificação marcada como lida"}

    def _enrich_reference(self, evento: dict):
        ref = evento.get("reference", {})
        ref_type = ref.get("type")

        if ref_type == "PRODUTO":
            ref["nome"] = self.produto_service.get_nome_produto(ref["id"])

        # futuros tipos aqui
