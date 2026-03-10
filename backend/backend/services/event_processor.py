# services/event_processor.py
from backend.services.notification_service import NotificationService
from backend.database.repository import Repository
from backend.services.notification_normalizer import normalize_event

class EventProcessor:

    def __init__(self, conn):
        self.repo = Repository(conn)
        self.notification_service = NotificationService(conn)

    def processar_evento(self, event_id: int):
        evento = self.repo.fetch_one(
            "notificacoes_eventos",
            "id",
            event_id
        )

        if not evento:
            return None

        self.notification_service.enrich_reference(evento)  

        notificacao = normalize_event(evento)
        if not notificacao:
            return None

        if not self.notification_service.should_notify(notificacao):
            return None

        return self.notification_service.criar_notificacao(notificacao)
