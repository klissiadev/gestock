from fastapi import APIRouter, Depends
from backend.database.base import get_connection
from backend.services.event_service import EventService

router = APIRouter(prefix="/eventos", tags=["Eventos"])


def get_service(conn = Depends(get_connection)):
    return EventService(conn)


@router.post("/")
def criar_evento(evento: dict, service: EventService = Depends(get_service)):
    return service.criar_evento(evento)


@router.get("/")
def listar_eventos(service: EventService = Depends(get_service)):
    return service.listar_eventos()

@router.get("/{event_id}")
def buscar_evento(event_id: int, service: EventService = Depends(get_service)):
    return service.buscar_por_id(event_id)
