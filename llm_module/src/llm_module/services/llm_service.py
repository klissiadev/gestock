from llm_module.models.chatbot import ChatBotService
import asyncio

class LLMService:
    def __init__(self):
        self.chatbot = ChatBotService()
        self._initialized = False
        self._init_lock = asyncio.Lock()

    async def _ensure_init(self):
        if not self._initialized:
            async with self._init_lock:
                if not self._initialized:
                    await self.chatbot.init()
                    self._initialized = True

    async def send_message(self, message: str, session_id: str | None):

        await self._ensure_init()

        if not session_id:
            raise ValueError("session_id obrigatório")

        resposta = await self.chatbot.send_message(
            user_input=message,
            session_id=session_id,
        )

        return resposta
    
    async def stream_message(
        self,
        message: str,
        session_id: str | None = None,
    ):
        await self._ensure_init()

        async for chunk in self.chatbot.stream_message(
            user_input=message,
            session_id=session_id,
        ):
            yield chunk

    async def ensure_session(self, session_id: str | None) -> str:
        """
        Garante que sempre exista uma sessão válida.
        - Cria se vier None
        - Cria se não existir no banco
        """

        if not session_id:
            return await self.create_session()

        exists = await self.session_exists(session_id)

        if not exists:
            return await self.create_session()

        return session_id