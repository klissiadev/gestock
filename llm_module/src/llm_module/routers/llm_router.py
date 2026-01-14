from fastapi import APIRouter
from pydantic import BaseModel
from llm_module.services.llm_service import LLMService

router = APIRouter(tags=["LLM"])
service = LLMService()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    user_id: str | None = None


@router.post("/chat")
async def chat_llm(payload: ChatRequest):
    response = await service.send_message(
        message=payload.message,
        session_id=payload.session_id,
        user_id=payload.user_id,
    )
    return {"response": response}