import os
import logging
import asyncio
from typing import List, Any

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_community.document_loaders import TextLoader
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.tools import tool
from pydantic import BaseModel

from llm_module.services.report_orchestrator import ReportOrchestratorService

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
load_dotenv()

class ReportToolSchema(BaseModel):
    report_type: str
    params: dict | None = None


# ======================================================
# CONFIG
# ======================================================

class Config:

    SYSTEM_PROMPT_LOCATION = os.getenv("SYSTEM_PROMPT_LOCATION")
    MAX_INPUT_SIZE = int(os.getenv("MAX_INPUT_LENGTH", "4000"))

    DB_USER = os.getenv("DB_LLM_USER")
    DB_PASSWORD = os.getenv("DB_LLM_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    DB_URI = (
        f"postgres://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?sslmode=require&channel_binding=require"
    )

    DB_URI_MASKED = (
        f"postgres://{DB_USER}:******"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?sslmode=require&channel_binding=require"
    )


# ======================================================
# CHATBOT RELATÓRIOS
# ======================================================

class ChatBotService:

    def __init__(self, test_mode: bool = True):

        # FLAG TESTE
        env_test_mode = os.getenv("LLM_TEST_MODE", "false").lower() == "true"
        self.test_mode = test_mode or env_test_mode

        # MODELOS
        self.main_model = ChatOllama(model="llama3.1:8b", temperature=0.0)
        self.summary_model = ChatOllama(model="gemma3:270m", temperature=0.0)

        # ORQUESTRADOR DE RELATÓRIOS
        self.report_orchestrator = ReportOrchestratorService()

        # TOOL OFICIAL DE RELATÓRIO
        @tool(return_direct=True)
        async def gerar_relatorio(
            report_type: str,
            params: dict | None = None,
            **kwargs
        ) -> str:
            """
            Utilize esta ferramenta quando o usuário solicitar relatórios.

            Tipos disponíveis:

            - estoque_baixo
            - giro_estoque
            - entradas_saidas
            - movimentacao_periodo
            - saldo_estoque
            - curva_abc
            - inventario
            - validade_proxima
            - produtos_sem_giro
            """

            try:

                if params is None:
                    params = {}

                params.update(kwargs)

                return await self.report_orchestrator.gerar_relatorio(
                    report_type=report_type,
                    params=params
                )

            except Exception as e:
                logger.error(f"Erro ao gerar relatório: {e}", exc_info=True)
                return "Erro ao gerar relatório."

        self.tools = [gerar_relatorio]

        self.agent = None
        self.memory_pool = self._prepare_db_pool()
        self.middleware = self._setup_middleware()
        self._background_tasks = set()

    # ======================================================
    # INFRA
    # ======================================================

    def _prepare_db_pool(self) -> AsyncConnectionPool:
        return AsyncConnectionPool(
            conninfo=Config.DB_URI,
            max_size=20,
            kwargs={
                "autocommit": True,
                "prepare_threshold": 0,
                "row_factory": dict_row,
            },
            open=False,
        )

    def _setup_middleware(self) -> List[SummarizationMiddleware]:
        return [
            SummarizationMiddleware(
                model=self.summary_model,
                trigger=("tokens", 5000),
                keep=("messages", 10),
            )
        ]

    # ======================================================
    # INIT
    # ======================================================

    async def init(self):

        await self.memory_pool.open()

        async with self.memory_pool.connection() as conn:
            await conn.execute("SELECT 1")

            checkpointer = AsyncPostgresSaver(conn)
            await checkpointer.setup()

            self.main_model = ChatOllama(
                model="llama3.1:8b",
                temperature=0.0
            ).bind_tools(self.tools)

            self.agent = create_agent(
                model=self.main_model,
                middleware=self.middleware,
                tools=self.tools,
                system_prompt=SystemMessage(content=self._load_system_prompt()),
                checkpointer=checkpointer,
            )

        return self

    # ======================================================
    # UTIL
    # ======================================================

    def _load_system_prompt(self) -> str:

        if not Config.SYSTEM_PROMPT_LOCATION:
            raise ValueError("SYSTEM_PROMPT_LOCATION não configurado")

        loader = TextLoader(Config.SYSTEM_PROMPT_LOCATION, encoding="utf-8")
        return loader.load()[0].page_content

    def _validate_input(self, text: str):

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Entrada inválida")

        if len(text.strip()) > Config.MAX_INPUT_SIZE:
            raise RuntimeError("Entrada muito grande")

    # ======================================================
    # SEND MESSAGE
    # ======================================================

    async def send_message(
        self,
        user_input: str,
        session_id: str = "guest",
    ) -> str:

        if not self.agent:
            raise RuntimeError("Serviço não inicializado")

        try:
            self._validate_input(user_input)

            result = await self.agent.ainvoke(
                {"messages": [HumanMessage(content=user_input)]},
                {"configurable": {"thread_id": session_id}},
            )

            bot_response = result["messages"][-1].content

            task = asyncio.create_task(
                self._save_log(session_id, user_input, bot_response)
            )

            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)

            return bot_response

        except Exception as e:
            logger.error(f"Erro na sessão {session_id}: {e}", exc_info=True)
            return "Erro interno ao processar a solicitação."

    # ======================================================
    # STREAM
    # ======================================================

    async def stream_message(self, user_input: str, session_id: str = "guest"):

        if not self.agent:
            raise RuntimeError("Agente não inicializado")

        self._validate_input(user_input)

        full_response = []

        async for chunk in self.agent.astream(
            {"messages": [HumanMessage(content=user_input)]},
            {"configurable": {"thread_id": session_id}},
            stream_mode="messages",
        ):

            content = chunk[0].content if isinstance(chunk, tuple) else chunk.content

            if content:
                full_response.append(content)
                yield content

        complete_text = "".join(full_response)

        task = asyncio.create_task(
            self._save_log(session_id, user_input, complete_text)
        )

        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    # ======================================================
    # LOG
    # ======================================================

    async def _save_log(self, session_id: str, user_input: str, bot_output: str):

        query = """
            INSERT INTO app_ai.conversation_logs
            (session_id, user_message, bot_response)
            VALUES (%s, %s, %s)
        """

        try:
            async with self.memory_pool.connection() as conn:
                await conn.execute(query, (session_id, user_input, bot_output))

        except Exception as e:
            logger.error(f"Falha ao salvar log: {e}")

    # ======================================================
    # CLOSE
    # ======================================================

    async def close(self):

        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

        if self.memory_pool:
            await self.memory_pool.close()
