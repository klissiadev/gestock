from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Annotated
from llm_module.services.llm_service import LLMService
from llm_module.services.llm_sessions import LLMSessionService
from fastapi.responses import StreamingResponse

from auth_module.utils.security import require_role
from auth_module.models.User import UserPublic

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

router = APIRouter(tags=["LLM"], prefix="/llm", dependencies=[Depends(require_role(["gestor"]))])

def get_llm_services(request: Request):
    llm_service = request.app.state.llm_service
    session_service = request.app.state.session_service
    return llm_service, session_service


async def task_generate_session_title(
    session_id: str, 
    first_message: str, 
    llm_service: LLMService, 
    session_service: LLMSessionService
):
    """Tarefa em background para geração de título."""
    current_title = await session_service.get_session_title(session_id)
    
    if not current_title or current_title in ["Nova Conversa", "Minerva"]:
        new_title = await llm_service.generate_title(first_message)
        await session_service.update_session_title(session_id, new_title)

# -------------------------
# CHAT (Síncrono)
# -------------------------
@router.post("/chat")
async def chat_llm(payload: ChatRequest,
                   user: Annotated[UserPublic, Depends(require_role(["gestor"]))],
                   services: Annotated[tuple, Depends(get_llm_services)],
                   background_tasks: BackgroundTasks
                   ):

    llm_service, session_service = services
    session_id = await session_service.ensure_session(payload.session_id, user.id)

    response = await llm_service.send_message(
        message=payload.message,
        session_id=session_id,
    )

    await session_service.touch_session(session_id)
    background_tasks.add_task(
        task_generate_session_title, 
        session_id, 
        payload.message, 
        llm_service, 
        session_service
    )

    return {
        "response": response,
        "session_id": session_id
    }

# -------------------------
# CHAT (Streaming)
# -------------------------
@router.post("/chat/stream")
async def chat_llm_stream(
    payload: ChatRequest,
    user: Annotated[UserPublic, Depends(require_role(["gestor"]))],
    services: Annotated[tuple, Depends(get_llm_services)],
    background_tasks: BackgroundTasks
):
    llm_service, session_service = services
    session_id = await session_service.ensure_session(payload.session_id, user.id)
    background_tasks.add_task(
        task_generate_session_title, 
        session_id, 
        payload.message, 
        llm_service, 
        session_service
    )

    async def generator():
        # 💡 O stream agora é gerenciado pelo LLMService, que também salva o log ao final
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


# -------------------------
# GESTÃO DE SESSÕES E TÍTULOS
# -------------------------
@router.get("/sessions")
async def list_sessions(user: Annotated[UserPublic, Depends(require_role(["gestor"]))],
                        services: Annotated[tuple, Depends(get_llm_services)]
                        ):
    session_service = services[1]
    return await session_service.list_sessions(user.id)

@router.post("/sessions")
async def new_session(user: Annotated[UserPublic, Depends(require_role(["gestor"]))],
                      services: Annotated[tuple, Depends(get_llm_services)]):
    _, session_service = services
    session_id = await session_service.create_session(user.id)
    return {"session_id": session_id}

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str,
                               user: Annotated[UserPublic, Depends(require_role(["gestor"]))],
                               services: Annotated[tuple, Depends(get_llm_services)], 
                               limit: int = 100, 
                               offset: int = 0):
    _, session_service = services
    if not await session_service.is_owner(session_id, user.id):
        raise HTTPException(status_code=403, detail="Acesso negado.")

    return await session_service.get_session_messages(session_id, limit, offset)


@router.get("/sessions/{session_id}/title")
async def get_session_title(session_id: str,
                            user: Annotated[UserPublic, Depends(require_role(["gestor"]))],
                            services: Annotated[tuple, Depends(get_llm_services)]):
    _, session_service = services
    if not await session_service.is_owner(session_id, user.id):
        raise HTTPException(status_code=403, detail="Acesso negado.")
    
    return await session_service.get_session_title(session_id)


