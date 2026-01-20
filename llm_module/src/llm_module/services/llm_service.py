from llm_module.models.chatbot import ChatBotService


class LLMService:
    def __init__(self):
        self.chatbot = ChatBotService()

    async def send_message(
        self,
        message: str,
        session_id: str | None = None,
    ) -> dict:
        
        await self.chatbot.init()
        resposta = await self.chatbot.send_message(
            user_input=message,
            session_id=session_id,
        )
        return resposta
