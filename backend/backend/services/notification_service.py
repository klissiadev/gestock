#services/notification_service.py
from fastapi import HTTPException
from backend.database.repository import Repository
from psycopg2.extras import Json
from backend.database.schemas import NotificationCreate
from backend.services.notification_normalizer import normalize_event

class NotificationService:

    def __init__(self, conn):
        self.conn = conn
        self.repo = Repository(conn)

    def from_event(self, event):
        if event.tipo == "IMPORTACAO_FINALIZADA":
            return NotificationDTO(
                type="IMPORTACAO",
                severity="success",
                title="Importação concluída",
                message=f"Arquivo {event.contexto['arquivo']} importado com sucesso",
                reference={"event_id": event.id},
                created_at=event.created_at,
                read=False
            )

    def processar_evento(self, event_id: int):
        
        # Busca evento
        evento = self.repo.fetch_one(
            "notificacoes_eventos",
            "id",
            event_id
        )

        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        # Verifica duplicidade
        ja_notificado = self.repo.fetch_one(
            "notificacoes",
            {"event_id": event_id}
        )

        if ja_notificado:
            return ja_notificado  

        # Normaliza
        notificacao = normalize_event(evento)

        if not notificacao:
            return None  # evento não gera notificação

        data = notificacao.dict()

        data["reference"] = Json(data["reference"])

        # Persiste
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
