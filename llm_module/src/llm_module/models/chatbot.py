import logging
from typing import List, Any
from datetime import datetime
from llm_module.utils.env_loader import load_env_from_root
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_community.document_loaders import TextLoader
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessageChunk
from llm_module.tools.tool_retriever import recuperar_tools_relevantes
from llm_module.tools.sql_tools import MINERVA_SQL_TOOLS
from llm_module.utils.config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
load_env_from_root()

# TO DO: Aplicação de RAG para as ferramentas da Minerva
    
class ChatBotService:
    def __init__(self):
        self.main_model = ChatOllama(model="qwen2.5:7B", temperature=0.0)
        self.summary_model = ChatOllama(model="gemma3:270m", temperature=0.0)
        self._initialized = False
        self.agent = None
        self.checkpointer = None
        
    async def init(self, checkpointer: AsyncPostgresSaver):
        """Inicializa o serviço salvando a persistência."""
        if self._initialized: return self
        self.agent = create_agent(
            model=self.main_model,
            tools=MINERVA_SQL_TOOLS,
            system_prompt=SystemMessage(content=self._load_system_prompt(MINERVA_SQL_TOOLS)),
            checkpointer=checkpointer, # 💡 Recebe o checkpointer pronto
        )
        self._initialized = True
        return self
    
    def _setup_middleware(self) -> List[SummarizationMiddleware]:
        return [
            SummarizationMiddleware(
                model=self.summary_model,
                trigger=("tokens", 5000),
                keep=("messages", 10)
            )
        ]
    
    def _load_system_prompt(self, tools_selecionadas: list) -> str:
        if not Config.SYSTEM_PROMPT_LOCATION:
            raise ValueError("Caminho do System Prompt não configurado no .env")
        
        loader = TextLoader(Config.SYSTEM_PROMPT_LOCATION, encoding='utf-8')
        raw_content = loader.load()[0].page_content

        # INJEÇÃO DINAMICA DE TEMPO
        agora = datetime.now()
        data_hoje = agora.strftime('%Y-%m-%d')
        dias_semana = {0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}
        dia_nome = dias_semana[agora.weekday()]
        content = raw_content.replace("{{DATA_HOJE}}", data_hoje)
        content = content.replace("{{DIA_SEMANA}}", dia_nome)

        # INJEÇÃO DINÂMICA DAS TOOLS
        texto_das_tools = "\n".join([f"- `{t.name}`: {t.description}" for t in tools_selecionadas])
        content = content.replace("{{FERRAMENTAS_DISPONIVEIS_AGORA}}", texto_das_tools)

        return content

    def _create_dynamic_agent(self, user_input: str):
        # Recupera apenas as 5 melhores tools para a pergunta
        # tools_filtradas = recuperar_tools_relevantes(user_input, limite=5)
        # print(f"[DEBUG] RAG selecionou as tools: {[t.name for t in tools_filtradas]}")
        
        # Gera o prompt instruindo a Minerva a usar APENAS essas 4
        prompt_dinamico = self._load_system_prompt(MINERVA_SQL_TOOLS)
        
        # Monta o agente 
        agent = create_agent(
            model=self.main_model,
            tools=MINERVA_SQL_TOOLS,
            system_prompt=SystemMessage(content=prompt_dinamico),
            checkpointer=self.checkpointer, 
            middleware=self._setup_middleware()
        )
        return agent
    
    async def send_message(self, user_input: str, session_id: str = "guest") -> Any:
        if not self._initialized:
            raise RuntimeError("Serviço não inicializado. Execute 'await service.init()'.")

        agente_dinamico = self._create_dynamic_agent(user_input)

        resultado = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            {"configurable": {"thread_id": session_id}},
        )
        
        print("=============================")
        print("Resposta completa do agente:")
        print(resultado)
        print("=============================")

        return resultado["messages"][-1].content
    
    async def stream_message(self, user_input: str, session_id: str = "guest"):
        if not self._initialized:
            raise RuntimeError("Agente não inicializado.")
        
        agente_dinamico = self._create_dynamic_agent(user_input)
        
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

    


        
