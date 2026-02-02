from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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

# Chat (EXISTENTE)

@router.post("/chat")
async def chat_llm(payload: ChatRequest):
    # se veio session_id, valida
    if payload.session_id and not session_exists(payload.session_id):
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    response = await service.send_message(
        message=payload.message,
        session_id=payload.session_id,
        user_id=payload.user_id,
    )
    return {"response": response}