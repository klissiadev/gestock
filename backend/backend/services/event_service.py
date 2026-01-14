from fastapi import HTTPException
from backend.database.repository import Repository


class EventService:

    def __init__(self, conn):
        self.repo = Repository(conn)

    def criar_evento(self, evento: dict):
        ok = self.repo.insert("eventos", produto)
        if not ok:
            raise HTTPException(status_code=400, detail="Erro ao registrar evento.")
        self.repo.commit()
        return {"message": "Evento registrado com sucesso"}

    def listar_eventos(self):
        cursor = self.repo.cursor
        cursor.execute("SELECT * FROM eventos")
        return cursor.fetchall()
