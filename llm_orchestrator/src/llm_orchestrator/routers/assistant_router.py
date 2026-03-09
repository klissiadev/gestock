from fastapi import APIRouter
from pydantic import BaseModel

from llm_orchestrator.services.router_service import RouterService
from llm_orchestrator.services.chat_client import ChatClient
from llm_orchestrator.services.report_client import ReportClient


router = APIRouter()

router_service = RouterService()
chat_client = ChatClient()
report_client = ReportClient()


class AssistantRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("/assistant")
async def assistant(request: AssistantRequest):

    agent = router_service.decide(request.message)

    if agent == "report":
        return await report_client.send(
            request.message,
            request.session_id
        )

    return await chat_client.send(
        request.message,
        request.session_id
    )