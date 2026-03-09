from fastapi import APIRouter, Depends
from backend.database.base import get_connection
from backend.database.repository import Repository
from backend.services.event_service import EventService
from backend.services.stock_event_service import StockEventService
from backend.services.expiration_event_service import ExpirationEventService
from auth_module.utils.security import get_current_user
from auth_module.models.User import UserPublic

router = APIRouter()

def get_stock_service(conn=Depends(get_connection)):
    event_service = EventService(conn)  
    repo = Repository(conn)              
    return StockEventService(repo, event_service)

def get_expiration_service(conn=Depends(get_connection)):
    event_service = EventService(conn)
    repo = Repository(conn)
    return ExpirationEventService(repo, event_service)

@router.post("/system/stock/check")
def check_stock_events(
    current_user: UserPublic = Depends(get_current_user),
    service: StockEventService = Depends(get_stock_service)
):
    service.check_stock_events(current_user.id)
    return {"status": "ok"}

@router.post("/system/expiration/check")
def check_expiration_events(
    current_user: UserPublic = Depends(get_current_user),
    service: ExpirationEventService = Depends(get_expiration_service)
):
    service.check_expiration_events(current_user.id)
    return {"status": "ok"}