from backend.database.repository import Repository
from backend.services.event_service import EventService
from backend.database.base import get_connection
from backend.database.schemas import NotificationEventCreate


class ExpirationEventService:

    def __init__(self, repo, event_service):
        self.repo = repo
        self.event_service = event_service

    def check_expiration_events(self, user_id: int):

        print("===== CHECK EXPIRATION EVENTS START =====")
        print("USER:", user_id)

        produtos = self.repo.execute_query("""
            SELECT id, nome, data_validade
            FROM app_core.vw_product
        """)

        print("TOTAL PRODUTOS ENCONTRADOS:", len(produtos))

        for produto in produtos:

            print("\n--- ANALISANDO PRODUTO ---")
            print("ID:", produto["id"])
            print("NOME:", produto["nome"])
            print("VALIDADE:", produto["data_validade"])

            event_payload = self._evaluate_product(produto)

            if not event_payload:
                print("→ Produto OK (sem evento)")
                continue

            print("→ EVENTO DETECTADO:", event_payload)

            if self._event_exists(produto["id"]):
                print("→ Evento já existe para esse produto, ignorando.")
                continue

            print("→ Criando evento...")

            event_obj = NotificationEventCreate(**event_payload)

            result = self.event_service.criar_evento(event_obj, user_id)

            print("→ Evento criado:", result)

        print("===== CHECK EXPIRATION EVENTS END =====")

    def _evaluate_product(self, produto):

        data_validade = produto["data_validade"]

        print("Checando validade:", data_validade)

        if not data_validade:
            print("→ Produto sem validade")
            return None

        from datetime import date

        hoje = date.today()

        print("Hoje:", hoje)

        if data_validade < hoje:
            state = "EXPIRED"
            print("→ Produto EXPIRADO")

        elif (data_validade - hoje).days <= 7:
            state = "EXPIRING_SOON"
            print("→ Produto vencendo em breve")

        else:
            print("→ Produto dentro do prazo")
            return None

        payload = {
            "type": "EXPIRATION",
            "context": {
                "state": state,
                "data": {
                    "expirationDate": str(data_validade)
                }
            },
            "reference": {
                "id": produto["id"],
                "type": "PRODUCT"
            }
        }

        print("Payload do evento:", payload)

        return payload

    def _event_exists(self, product_id):

        print("Checando se evento já existe para produto:", product_id)

        sql = """
            SELECT *
            FROM app_core.notificacoes_eventos
            WHERE reference->>'id' = %s
            AND type = 'EXPIRATION'
            LIMIT 1
        """

        result = self.repo.fetch_one_raw(sql, (str(product_id),))

        print("Resultado da busca:", result)

        return result is not None