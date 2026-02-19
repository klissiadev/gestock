from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Annotated
from llm_module.services.llm_service import LLMService
from llm_module.services.llm_sessions import LLMSessionService
from fastapi.responses import StreamingResponse

from auth_module.utils.security import get_current_user
from auth_module.models.User import UserPublic

router = APIRouter(tags=["LLM"], prefix="/llm", dependencies=[Depends(get_current_user)])

llm_service = LLMService()
session_service = LLMSessionService(llm_service)

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

async def task_generate_session_title(session_id: str, first_message: str):
    """Tarefa que roda em background. Gerador de titulo: verifica se ja tem, senao, cria outro"""

    print("Gerando titulo")
    current_title = await session_service.get_session_title(session_id)
    
    if not current_title or current_title == "Nova Conversa":
        new_title = await llm_service.generate_title(first_message)
        await session_service.update_session_title(session_id, new_title)

# -------------------------
# CHAT
# -------------------------
@router.post("/chat")
async def chat_llm(payload: ChatRequest,
                   user: Annotated[UserPublic, Depends(get_current_user)],
                   background_tasks: BackgroundTasks
                   ):

    session_id = await session_service.ensure_session(session_id=payload.session_id, user_id=user.id)

    response = await llm_service.send_message(
        message=payload.message,
        session_id=session_id,
    )

    await session_service.touch_session(session_id)
    background_tasks.add_task(task_generate_session_title, session_id, payload.message)

    return {
        "response": response,
        "session_id": session_id
    }


# -------------------------
# LISTAR SESSÕES
# -------------------------
@router.get("/sessions")
async def list_sessions(user: Annotated[UserPublic, Depends(get_current_user)]):
    return await session_service.list_sessions(user.id)


# -------------------------
# CRIAR SESSÃO
# -------------------------
@router.post("/sessions")
async def new_session(user: Annotated[UserPublic, Depends(get_current_user)]):
    session_id = await session_service.create_session(user.id)
    return {"session_id": session_id}


# -------------------------
# MENSAGENS DA SESSÃO
# ------------------------
@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str,
                               user: Annotated[UserPublic, Depends(get_current_user)], 
                               limit: int = 100, 
                               offset: int = 0,
                            ):

    if not await session_service.is_owner(session_id, user.id):
        raise HTTPException(
            status_code=404, 
            detail="Você não tem permissão para acessar esta sessão."
        )

    return await session_service.get_session_messages(
        session_id=session_id,
        limit=limit,
        offset=offset
    )


@router.post("/chat/stream")
async def chat_llm_stream(
    payload: ChatRequest,
    user: Annotated[UserPublic, Depends(get_current_user)],
    background_tasks: BackgroundTasks
):
    session_id = await session_service.ensure_session(payload.session_id, user_id=user.id)
    background_tasks.add_task(task_generate_session_title, session_id, payload.message)

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
async def get_session_title(session_id: str,
                            user: Annotated[UserPublic, Depends(get_current_user)]):
    if not await session_service.is_owner(session_id, user.id):
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    return await session_service.get_session_title(session_id)