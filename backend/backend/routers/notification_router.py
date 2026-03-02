#routers/notification_router.py
from fastapi import APIRouter, Depends
from backend.database.base import get_connection
from backend.services.notification_service import NotificationService
from backend.database.schemas import NotificationCreate
from auth_module.utils.security import get_current_user
from auth_module.models.User import UserPublic
from uuid import UUID

router = APIRouter(prefix="/notificacoes", tags=["Notificacoes"])

def get_service(conn=Depends(get_connection)):
    return NotificationService(conn)

@router.post("/from-event/{event_id}")
def criar_notificacao_do_evento(
    event_id: int,
    current_user: UserPublic = Depends(get_current_user),
    service: NotificationService = Depends(get_service)
):
    return service.processar_evento(event_id, current_user.id)

@router.get("/notificacoes/from-event/{event_id}")
def get_notification_from_event(event_id: int):
    event = event_repo.get(event_id)
    return notification_service.from_event(event)

@router.get("/")
def listar_notificacoes(
    read: bool | None = None,
    limit: int = 20,
    cursor: str | None = None,
    current_user = Depends(get_current_user),
    service: NotificationService = Depends(get_service)
):
    return service.listar_notificacoes(
        user_id=current_user.id,
        read=read,
        limit=limit,
        cursor=cursor
    )

@router.get("/{notification_id}")
def buscar_notificacao(
    notification_id: int,
    current_user = Depends(get_current_user),
    service: NotificationService = Depends(get_service)
):
    return service.buscar_por_id(
        notification_id,
        current_user.id
    )

@router.patch("/{notification_id}/read")
def marcar_como_lida(
    notification_id: int,
    current_user = Depends(get_current_user),
    service: NotificationService = Depends(get_service)
):
    return service.marcar_como_lida(
        notification_id,
        current_user.id
    )