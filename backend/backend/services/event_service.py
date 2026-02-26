#services/event_service.py
from fastapi import HTTPException
from backend.database.repository import Repository
from psycopg2.extras import Json
from backend.database.schemas import NotificationEventCreate

class EventService:

    def __init__(self, conn):
        self.repo = Repository(conn)

    def criar_evento(self, evento: NotificationEventCreate):
        data = evento.dict()
        
        data["context"] = Json(data["context"])
        data["reference"] = Json(data["reference"])

        ok = self.repo.insert(
            "app_core.notificacoes_eventos",
            data
        )

        if not ok:
            raise HTTPException(status_code=400, detail="Erro ao registrar evento.")

        self.repo.commit()
        return {"message": "Evento registrado com sucesso"}

    def listar_eventos(self):
        sql = """
            SELECT *
            FROM app_core.notificacoes_eventos
            ORDER BY created_at DESC
        """
        self.repo.cursor.execute(sql)
        return self.repo.cursor.fetchall()

    def buscar_por_id(self, event_id: int):
        evento = self.repo.fetch_one(
            "notificacoes_eventos",
            "id",
            event_id
        )
        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        return evento
