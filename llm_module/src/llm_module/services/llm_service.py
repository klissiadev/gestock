from llm_module.models.chatbot import ChatBotService
import asyncio
import logging

from llm_module.models.title_generator import TitleGeneratorService
from llm_module.audit.logger import AuditLogger
from llm_module.database.checkpointer import CheckpointerFactory

from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)

class LLMService:
    """Orquestrador do Chatbot"""
    def __init__(self, connection_pool):
        self.database_pool : AsyncConnectionPool = connection_pool
        self.chatbot = ChatBotService()
        self.title_gen = TitleGeneratorService()
        self.audit = AuditLogger(self.database_pool)
        self._initialized = False
        self._init_lock = asyncio.Lock()
        self._background_task = set()


    async def ensure_init(self):
        """Inicializa a infraestrutura de IA e persistência uma única vez."""
        if not self._initialized:
            async with self._init_lock:
                if not self._initialized:
                    try:
                        checkpointer = await CheckpointerFactory.create(self.database_pool)
                        await self.chatbot.init(checkpointer=checkpointer)
                        self._initialized = True
                    except Exception as e:
                        logger.error(f"Falha na inicialização do LLMService: {e}")
                        raise


    async def send_message(self, message: str, session_id: str):
        """Orquestra o envio de mensagem e a gravação de auditoria."""
        await self.ensure_init()

        if not session_id:
            raise ValueError("session_id obrigatório")

        resposta = await self.chatbot.send_message(
            user_input=message,
            session_id=session_id,
        )

        self._background_task.add(asyncio.create_task(self.audit.save_conversation(session_id, message, resposta)))

        return resposta
    

    async def stream_message(
        self,
        message: str,
        session_id: str | None = None,
    ):
        """Orquestra o streaming e captura o texto final para o log."""
        await self.ensure_init()

        full_response = []

        async for chunk in self.chatbot.stream_message(
            user_input=message,
            session_id=session_id,
        ):
            if chunk:
                full_response.append(chunk)
            yield chunk
        
        complete_text = "".join(full_response)
        self._background_task.add(asyncio.create_task(self.audit.save_conversation(session_id, message, complete_text)))


    async def generate_title(self, text: str) -> str:
        """Delega a geração de título para o serviço especializado."""
        return await self.title_gen.generate_title(text)


    async def close(self):
        """Aguarda a conclusão das auditorias e encerra os serviços."""
        if self._background_task:
            logger.info(f"Aguardando {len(self._background_task)} tarefas de auditoria...")
            await asyncio.gather(*self._background_task, return_exceptions=True)
        
        logger.info("LLMService encerrado com segurança.")

    
    