import os
import logging
import asyncio
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_community.document_loaders import TextLoader
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from langchain_core.messages import SystemMessage, HumanMessage

from llm_module.tools.sql_tools import (
    tool_buscar_produto,
    tool_listar_produtos,
    tool_buscar_movimentacao,
    tool_calcular_validade,
    tool_listar_movimentacoes,
    buscar_produtos_a_vencer,
    buscar_produtos_abaixo_estoque,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
load_dotenv()

class Config:
    """Centraliza as configurações do ambiente."""
    SYSTEM_PROMPT_LOCATION = os.getenv("SYSTEM_PROMPT_LOCATION")
    MAX_INPUT_SIZE = int(os.getenv("MAX_INPUT_LENGTH", "4000"))
    
    # Adicione ?sslmode=require ao final da URL
    DB_URI = (
        f"postgres://{os.getenv('DB_LLM_USER')}:{os.getenv('DB_LLM_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        f"?sslmode=require&channel_binding=require"
    )

    
class ChatBotService:
    def __init__(self):
        self.main_model = ChatOllama(model="qwen2.5:7B", temperature=0.0)
        self.summary_model = ChatOllama(model="gemma3:270m", temperature=0.0)
        
        self.tools = [
            buscar_produtos_a_vencer, tool_buscar_movimentacao, 
            tool_buscar_produto, tool_listar_produtos, 
            tool_calcular_validade, tool_listar_movimentacoes, 
            buscar_produtos_abaixo_estoque
        ]
        
        self.agent = None
        self.memory_pool = self._prepare_db_pool()
        self.middleware = self._setup_middleware()
        self._background_tasks = set()
        
    def _prepare_db_pool(self) -> AsyncConnectionPool:
        return AsyncConnectionPool(
            conninfo=Config.DB_URI,
            max_size=20,
            kwargs={
                "autocommit": True,
                "prepare_threshold": 0,
                "row_factory": dict_row,
            },
            open=False
        )
        
    def _setup_middleware(self) -> List[SummarizationMiddleware]:
        return [
            SummarizationMiddleware(
                model=self.summary_model,
                trigger=("tokens", 5000),
                keep=("messages", 10)
            )
        ]
        
    async def init(self):
        """Inicializa conexões assíncronas e o agente."""
        await self.memory_pool.open()
        
        async with self.memory_pool.connection() as conn:
            await conn.execute("SELECT 1")
        
        # Setup de Memoria do agente
        conn = await self.memory_pool.getconn() 
        checkpointer = AsyncPostgresSaver(conn)
        await checkpointer.setup()
        
        # Criacao do agente
        self.agent = create_agent(
            model=self.main_model,
            middleware=self.middleware,
            tools=self.tools,
            system_prompt=SystemMessage(content=self._load_system_prompt()),
            checkpointer=checkpointer,
        )
        return self
    
    def _load_system_prompt(self) -> str:
        if not Config.SYSTEM_PROMPT_LOCATION:
            raise ValueError("Caminho do System Prompt não configurado no .env")
        
        loader = TextLoader(Config.SYSTEM_PROMPT_LOCATION, encoding='utf-8')
        return loader.load()[0].page_content
    
    def _validate_input(self, text: str):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("A entrada deve ser uma string não vazia.")
        
        if len(text.strip()) > Config.MAX_INPUT_SIZE:
            raise RuntimeError(f"Entrada excede o limite de {Config.MAX_INPUT_SIZE} caracteres.")

    async def send_message(self, user_input: str, session_id: str = "guest") -> Any:
        if not self.agent:
            raise RuntimeError("Serviço não inicializado. Execute 'await service.init()'.")

        try:
            self._validate_input(user_input)

            result = await self.agent.ainvoke(
                {"messages": [HumanMessage(content=user_input)]},
                {"configurable": {"thread_id": session_id}},
            )
            
            bot_response = result["messages"][-1].content
            
            # Agenda o armazenamento de logs no banco de dados e protege de ser morto pelo GC
            task = asyncio.create_task(
                self._save_log(session_id, user_input, bot_response)
            )
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)
            
            return result["messages"][-1].content

        except Exception as e:
            logger.error(f"Erro na sessão {session_id}: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "session_id": session_id,
                "response": "Desculpe, ocorreu um erro interno.",
                "details": str(e)
            }
            
    async def close(self):
        """Fecha as conexões e aguarda tarefas pendentes."""
        if self._background_tasks:
            # Aguarda todas as tarefas de log pendentes terminarem
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

        if self.memory_pool:
            await self.memory_pool.close()
            logger.info("Serviço encerrado com segurança.")

    async def _save_log(self, session_id: str, user_input: str, bot_output: str):
        """Armazena a interacao em texto puro num banco de dados"""
        query = """
            INSERT INTO app_ai.conversation_logs (session_id, user_message, bot_response)
            VALUES (%s, %s, %s)
        """
        try:
            async with self.memory_pool.connection() as conn:
                await conn.execute(query, (session_id, user_input, bot_output))
        except Exception as e:
            logger.error(f"Falha ao salvar log legível: {e}")

    async def stream_message(self, user_input: str, session_id: str = "guest"):
        if not self.agent:
            raise RuntimeError("Agente não inicializado.")

        self._validate_input(user_input)
        
        full_response = []
        
        # O astream retorna um gerador assíncrono de eventos
        async for chunk in self.agent.astream(
            {"messages": [HumanMessage(content=user_input)]},
            {"configurable": {"thread_id": session_id}},
            stream_mode="messages" # Foca apenas nos chunks de mensagens
        ):
            # No LangGraph, o chunk geralmente vem como uma tupla (mensagem, metadados)
            # ou diretamente o conteúdo dependendo da versão
            content = chunk[0].content if isinstance(chunk, tuple) else chunk.content
            
            if content:
                full_response.append(content)
                yield content # Envia o pedaço de texto para o cliente imediatamente

        # --- Logging após o streaming terminar ---
        complete_text = "".join(full_response)
        task = asyncio.create_task(
            self._save_log(session_id, user_input, complete_text)
        )
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

"""
Bloco de testes, um exemplo de como chamar a Minerva
"""
async def main():
    chatbot = ChatBotService()
    await chatbot.init()
    try:
        print("Minerva: ", end="", flush=True)
        
        # Como stream_message tem 'yield', usamos 'async for'
        async for chunk in chatbot.stream_message("Olá, Minerva! Eu sou o Pedro", session_id="user_123"):
            print(chunk, end="", flush=True)
            
        print() # Apenas para pular linha ao final da resposta
    finally:
        await chatbot.close()
        
if __name__ == "__main__":
    # Detecta se é Windows para aplicar a correção de loop
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot desligado pelo usuário.")
    


        
