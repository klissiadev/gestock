from fastapi import FastAPI, APIRouter, BackgroundTasks
from backend.services.mail_service import mail_service

router = APIRouter(prefix="/triggerMail", tags=["mail"])

@router.post(path="/", summary="Aciona o e-mail de alerta")
async def send_alert(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(mail_service)
        return {"status": "Email agendado para envio"}
    except Exception:
        return {"status": "Falha ao agendar envio"}
        
    