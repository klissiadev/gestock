from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from llm_module.services.llm_service import LLMService
from llm_module.services.llm_sessions import LLMSessionService
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["LLM"])
llm_service = LLMService()
session_service = LLMSessionService(llm_service)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


# -------------------------
# CHAT
# -------------------------
@router.post("/chat")
async def chat_llm(payload: ChatRequest):

    if payload.session_id:
        exists = await session_service.session_exists(payload.session_id)

        if not exists:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")

    response = await llm_service.send_message(
        message=payload.message,
        session_id=payload.session_id,
    )

    return {
        "response": response,
        "session_id": payload.session_id,
    }


# -------------------------
# LISTAR SESSÕES
# -------------------------
@router.get("/sessions")
async def get_sessions():
    return await session_service.list_sessions()


# -------------------------
# CRIAR SESSÃO
# -------------------------
@router.post("/sessions")
def new_session():
    session_id = session_service.create_session()
    return {"session_id": session_id}


# -------------------------
# MENSAGENS DA SESSÃO
# ------------------------
@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    limit: int = 100,
    offset: int = 0
):

    exists = await session_service.session_exists(session_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    return await session_service.get_session_messages(
        session_id=session_id,
        limit=limit,
        offset=offset
    )


@router.post("/chat/stream")
async def chat_llm_stream(payload: ChatRequest):

    async def generator():
        async for chunk in llm_service.stream_message(
            message=payload.message,
            session_id=payload.session_id,
        ):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")