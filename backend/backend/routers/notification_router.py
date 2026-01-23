# routers/notification_router.py
from fastapi import APIRouter, Depends
from backend.database.base import get_connection
from backend.services.notification_service import NotificationService

router = APIRouter(prefix="/notificacoes", tags=["Notificacoes"])

def get_service(conn=Depends(get_connection)):
    return NotificationService(conn)

@router.get("/")
def listar_notificacoes(
    read: bool | None = None,
    limit: int = 20,
    cursor: str | None = None,
    service: NotificationService = Depends(get_service)
):
    return service.listar_notificacoes(
        read=read,
        limit=limit,
        cursor=cursor
    )

@router.get("/{notification_id}")
def buscar_notificacao(
    notification_id: int,
    service: NotificationService = Depends(get_service)
):
    return service.buscar_por_id(notification_id)

@router.patch("/{notification_id}/read")
def marcar_como_lida(
    notification_id: int,
    service: NotificationService = Depends(get_service)
):
    return service.marcar_como_lida(notification_id)
