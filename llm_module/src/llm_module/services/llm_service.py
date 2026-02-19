from llm_module.models.chatbot import ChatBotService
import asyncio

class LLMService:
    def __init__(self):
        self.chatbot = ChatBotService()
        self._initialized = False
        self._init_lock = asyncio.Lock()

    async def ensure_init(self):
        if not self._initialized:
            async with self._init_lock:
                if not self._initialized:
                    await self.chatbot.init()
                    self._initialized = True

    async def send_message(self, message: str, session_id: str | None):
        await self.ensure_init()

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
        await self.ensure_init()

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
        await self.ensure_init()

        if not session_id:
            return await self.create_session()

        exists = await self.session_exists(session_id)

        if not exists:
            return await self.create_session()

        return session_id
    
    async def generate_title(self, text: str) -> str:
        await self.ensure_init()
        
        """Gera um título curto usando o modelo de sumerização."""
        prompt = (
            "Você é um assistente de indexação. Resuma a intenção do usuário em um título de 2 a 4 palavras.\n"
            "Regras: Responda APENAS o título. Sem pontuação. Sem explicações.\n\n"
            f"Entrada: '{text[:300]}'\n"
            "Título:"
        )
        try:
            res = await self.chatbot.summary_model.ainvoke(prompt)
            title = res.content.strip().split('\n')[0].replace('"', '').replace('.', '')
            return title if len(title) > 2 else "Nova Conversa"
        except Exception as e:
            return "Nova Conversa"
