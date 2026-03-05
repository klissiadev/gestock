# services/event_service.py
from fastapi import HTTPException
from backend.database.repository import Repository
from psycopg2.extras import Json
from backend.database.schemas import NotificationEventCreate
from uuid import UUID

class EventService:

    def __init__(self, conn):
        self.repo = Repository(conn)

    def criar_evento(self, evento: NotificationEventCreate, user_id: UUID):
        data = evento.dict()

        type_ = data.get("type")

        # Regras específicas por tipo (ANTES de converter para Json)
        if type_ == "RUPTURE":
            if not self._should_create_rupture(data):
                return None

        # Só depois que passou nas regras, prepara para persistência
        data["user_id"] = user_id
        data["context"] = Json(data["context"])
        data["reference"] = Json(data["reference"])

        result = self.repo.insert_returning(
            table="app_core.notificacoes_eventos",
            data=data,
            returning="id"
        )

        if not result:
            raise HTTPException(
                status_code=400,
                detail="Erro ao registrar evento."
            )

        if isinstance(result, tuple):
            evento_id = result[0]
        elif isinstance(result, dict):
            evento_id = result.get("id")
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
            table="app_core.notificacoes_eventos",
            conditions={"id": event_id}
        )

        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        return evento

    def _ultimo_evento_ruptura(self, product_id: int):
        result = self.repo.execute_query("""
            SELECT context
            FROM app_core.notificacoes_eventos
            WHERE type = 'RUPTURE'
            AND reference->>'id' = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (str(product_id),))

        return result[0] if result else None

    def _should_create_rupture(self, data: dict) -> bool:
        reference = data.get("reference") or {}
        context = data.get("context") or {}

        product_id = reference.get("id")
        if not product_id:
            return True

        ultimo_evento = self._ultimo_evento_ruptura(product_id)

        if not ultimo_evento:
            return True

        ultimo_context = ultimo_evento.get("context") or {}
        ultimo_data = ultimo_context.get("data") or {}

        ultimo_estoque = ultimo_data.get("currentStock")
        estoque_atual = (context.get("data") or {}).get("currentStock")

        ultimo_state = ultimo_context.get("state")
        state_atual = context.get("state")

        # Se qualquer um for None, deixa criar
        if estoque_atual is None:
            return True

        if ultimo_estoque == estoque_atual and ultimo_state == state_atual:
            return False

        return True