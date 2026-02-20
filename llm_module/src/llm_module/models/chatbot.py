import os
import logging
import asyncio
import token
from typing import Optional, List, Dict, Any

from llm_module.utils.env_loader import load_env_from_root
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_community.document_loaders import TextLoader
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from langchain_core.messages import SystemMessage, HumanMessage, AIMessageChunk
from llm_module.tools.sql_tools import (
    tool_buscar_produto,
    tool_listar_produtos,
    tool_buscar_movimentacao,
    tool_calcular_validade,
    tool_listar_movimentacoes,
    buscar_produtos_a_vencer,
    buscar_produtos_abaixo_estoque,
)
from llm_module.utils.config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
load_env_from_root()

    
class ChatBotService:
    def __init__(self):
        self.main_model = ChatOllama(model="qwen2.5:7B", temperature=0.0)
        self.summary_model = ChatOllama(model="gemma3:270m", temperature=0.0)
        self._initialized = False
        self.agent = None
        self.tools = [
            buscar_produtos_a_vencer, tool_buscar_movimentacao, 
            tool_buscar_produto, tool_listar_produtos, 
            tool_calcular_validade, tool_listar_movimentacoes, 
            buscar_produtos_abaixo_estoque
        ]
        
    def _setup_middleware(self) -> List[SummarizationMiddleware]:
        return [
            SummarizationMiddleware(
                model=self.summary_model,
                trigger=("tokens", 5000),
                keep=("messages", 10)
            )
        ]
        
    async def init(self, checkpointer: AsyncPostgresSaver):
        """Inicializa o agente de forma segura."""
        if self._initialized: return self

        self.agent = create_agent(
            model=self.main_model,
            tools=self.tools,
            system_prompt=SystemMessage(content=self._load_system_prompt()),
            checkpointer=checkpointer, # 💡 Recebe o checkpointer pronto
        )
        self._initialized = True
        return self
    
    def _load_system_prompt(self) -> str:
        if not Config.SYSTEM_PROMPT_LOCATION:
            raise ValueError("Caminho do System Prompt não configurado no .env")
        
        loader = TextLoader(Config.SYSTEM_PROMPT_LOCATION, encoding='utf-8')
        return loader.load()[0].page_content

    async def send_message(self, user_input: str, session_id: str = "guest") -> Any:
        if not self.agent:
            raise RuntimeError("Serviço não inicializado. Execute 'await service.init()'.")

        resultado = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            {"configurable": {"thread_id": session_id}},
        )

        return resultado["messages"][-1].content
    
    async def stream_message(self, user_input: str, session_id: str = "guest"):
        if not self.agent:
            raise RuntimeError("Agente não inicializado.")
        
        full_response = []
        async for token, metadata in self.agent.astream(
            {"messages": [HumanMessage(content=user_input)]},
            {"configurable": {"thread_id": session_id}},
            stream_mode="messages" 
        ):
            if not isinstance(token, AIMessageChunk):
                continue
            text = token.text
            if text:
                full_response.append(text)
                yield text

    


        
