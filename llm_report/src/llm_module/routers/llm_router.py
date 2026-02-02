from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from reports.report_intent import detect_report
from reports.report_repository import ReportRepository
from reports.report_service import ReportService
from llm_module.services.llm_service import LLMService
from llm_module.services.llm_sessions import (
    list_sessions,
    create_session,
    session_exists
)

router = APIRouter(tags=["LLM"])
service = LLMService()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("/chat")
async def chat_llm(payload: ChatRequest):
    print("CHEGOU:", payload)
    # valida sessão se vier
    if payload.session_id and not session_exists(payload.session_id):
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    # Detecta se é pedido de relatório
    intent = detect_report(payload.message)
    print("INTENT DETECTADO:", intent)
    # Se for relatório, não chama a LLM
    if intent:
        repository = ReportRepository()
        report_service = ReportService(repository)

        report = report_service.generate(
            report_type=intent["report_type"],
            params=intent.get("params", {})
        )

        return {
            "answer": "",
            "session_id": payload.session_id,
            "payload": report,
        }

    # Caso contrário, segue fluxo normal da LLM
    answer = await service.send_message(
        message=payload.message,
        session_id=payload.session_id,
    )

    return {
        "answer": answer,
        "session_id": payload.session_id,
    }


# Sessões (TESTE)

@router.get("/sessions")
def get_sessions():
    return list_sessions()


@router.post("/sessions")
def new_session():
    session_id = create_session()
    return {"session_id": session_id}
