from backend.database.repository import Repository
from backend.services.event_service import EventService
from backend.database.base import get_connection
from backend.database.schemas import NotificationEventCreate



class StockEventService:

    def __init__(self, repo, event_service):
        self.repo = repo
        self.event_service = event_service

    def check_stock_events(self, user_id: int):
        produtos = self.repo.execute_query("""
            SELECT id, nome, estoque_atual, estoque_minimo
            FROM app_core.vw_product
        """)

        for produto in produtos:
            event_payload = self._evaluate_product(produto)

            if not event_payload:
                continue

            if self._event_exists(produto["id"], event_payload["context"]["state"]):
                continue

            print(type(event_payload), event_payload)
            event_obj = NotificationEventCreate(**event_payload)

            self.event_service.criar_evento(event_obj, user_id)

    def _evaluate_product(self, produto):
        estoque = produto["estoque_atual"]
        minimo = produto["estoque_minimo"]

        if estoque is None or minimo is None:
            return None

        if estoque <= minimo:
            state = "BELOW_MINIMUM"
        elif estoque > minimo and estoque <= (minimo * 1.10):
            state = "NEAR_MINIMUM"
        else:
            return None

        return {
            "type": "RUPTURE",
            "context": {
                "state": state,
                "data": {
                    "currentStock": estoque,
                    "minimumStock": minimo
                }
            },
            "reference": {
                "id": produto["id"],
                "type": "PRODUCT"
            }
        }

        return None
    
    def _event_exists(self, product_id, state):
        sql = """
            SELECT *
            FROM app_core.notificacoes_eventos
            WHERE reference->>'id' = %s
            AND context->>'state' = %s
            LIMIT 1
        """

        return self.repo.fetch_one_raw(sql, (str(product_id), state))


