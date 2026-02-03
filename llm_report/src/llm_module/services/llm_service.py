from llm_module.models.chatbot import ChatBotService


class LLMService:
    def __init__(self):
        self.chatbot = ChatBotService()
        self._initialized = False

    async def init(self):
        if not self._initialized:
            await self.chatbot.init()
            self._initialized = True

    async def send_message(
        self,
        message: str,
        session_id: str | None = None,
    ) -> str:
        await self.init()

        return await self.chatbot.send_message(
            user_input=message,
            session_id=session_id,
        )

    async def close(self):
        if self._initialized:
            await self.chatbot.close()
