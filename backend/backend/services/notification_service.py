#services/notification_service.py
from fastapi import HTTPException
from backend.database.repository import Repository
from psycopg2.extras import Json
from backend.database.schemas import NotificationCreate

class NotificationService:

    def __init__(self, conn):
        self.repo = Repository(conn)

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

    def listar_notificacoes(self):
        sql = """
            SELECT *
            FROM app_core.notificacoes
            ORDER BY created_at DESC
        """
        self.repo.cursor.execute(sql)
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
