# services/event_service.py
from fastapi import HTTPException
from backend.database.repository import Repository
from psycopg2.extras import Json
from backend.database.schemas import NotificationEventCreate

class EventService:

    def __init__(self, conn):
        self.repo = Repository(conn)

    def criar_evento(self, evento: dict | NotificationEventCreate) -> int:
        data = evento.dict() if isinstance(evento, NotificationEventCreate) else evento

        data["context"] = Json(data["context"])
        data["reference"] = Json(data["reference"])

        result = self.repo.insert_returning(
            table="app_core.notificacoes_eventos",
            data=data,
            returning="id"
        )

        # 🔒 Blindagem contra retorno inconsistente
        if not result:
            raise HTTPException(
                status_code=400,
                detail="Erro ao registrar evento."
            )

        # Se vier tupla (ex: (42,))
        if isinstance(result, tuple):
            evento_id = result[0]

        # Se vier dict (caso mude no futuro)
        elif isinstance(result, dict):
            evento_id = result.get("id")

        # Se vier valor direto
        else:
            evento_id = result

        if not evento_id:
            raise HTTPException(
                status_code=500,
                detail="Evento criado, mas ID inválido."
            )

        self.repo.commit()
        return evento_id

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
