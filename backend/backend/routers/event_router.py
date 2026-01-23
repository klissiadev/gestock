#backend\backend\routers\event_router.py
from fastapi import APIRouter, Depends, Request
from backend.database.base import get_connection
from backend.services.event_service import EventService
from backend.services.event_processor import EventProcessor
from backend.database.schemas import NotificationEventCreate

router = APIRouter(prefix="/eventos", tags=["Eventos"])


def get_service(conn = Depends(get_connection)):
    return EventService(conn)

@router.post("/")
def criar_evento(
    evento: NotificationEventCreate,
    request: Request,
    service: EventService = Depends(get_service)
):
    event_id = service.criar_evento(evento)

    return {
        "id": event_id,
        "message": "Evento registrado com sucesso"
    }



@router.get("/")
def listar_eventos(service: EventService = Depends(get_service)):
    return service.listar_eventos()

@router.get("/{event_id}")
def buscar_evento(event_id: int, service: EventService = Depends(get_service)):
    return service.buscar_por_id(event_id)


@router.post("/eventos/{event_id}/processar")
def processar_evento(
    event_id: int,
    conn = Depends(get_connection)
):
    processor = EventProcessor(conn)
    return processor.processar_evento(event_id)
