from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from llm_module.services.llm_service import LLMService
from llm_module.services.llm_sessions import LLMSessionService
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["LLM"], prefix="/llm")
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

    session_id = await session_service.ensure_session(payload.session_id)

    response = await llm_service.send_message(
        message=payload.message,
        session_id=session_id,
    )

    await session_service.touch_session(session_id)

    return {
        "response": response,
        "session_id": session_id
    }


# -------------------------
# LISTAR SESSÕES
# -------------------------
@router.get("/sessions")
async def list_sessions():
    return await session_service.list_sessions()


# -------------------------
# CRIAR SESSÃO
# -------------------------
@router.post("/sessions")
async def new_session():
    session_id = await session_service.create_session()
    return {"session_id": session_id}


# -------------------------
# MENSAGENS DA SESSÃO
# ------------------------
@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str, limit: int = 100, offset: int = 0):

    exists = await session_service.session_exists(session_id)

    if not exists:
        return []

    return await session_service.get_session_messages(
        session_id=session_id,
        limit=limit,
        offset=offset
    )


@router.post("/chat/stream")
async def chat_llm_stream(payload: ChatRequest):

    session_id = await session_service.ensure_session(payload.session_id)

    async def generator():

        async for chunk in llm_service.stream_message(
            message=payload.message,
            session_id=session_id,
        ):
            yield chunk.encode("utf-8") if isinstance(chunk, str) else chunk

        await session_service.touch_session(session_id)

    return StreamingResponse(
        generator(),
        media_type="text/plain",
        headers={"X-Session-Id": session_id}
    )
    
@router.get("/sessions/{session_id}/title")
async def get_session_title(session_id: str):
    return await session_service.get_session_title(session_id)