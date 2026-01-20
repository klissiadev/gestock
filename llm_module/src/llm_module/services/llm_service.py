from llm_module.models.chatbot import chat_bot_service


class LLMService:
    def __init__(self):
        self.chatbot = chat_bot_service()

    async def send_message(
        self,
        message: str,
        session_id: str | None = None,
    ) -> dict:
        resposta = await self.chatbot.send_message(
            user_input=message,
            session_id=session_id,
        )
        return resposta
