from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import SystemMessage
from langchain.messages import HumanMessage
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os, time, uuid

from llm_module.tools.mcp_tools import tool_get_current_time
from llm_module.tools.mcp_tools import tool_calcular_validade
from llm_module.tools.sql_tools import tool_consultar_estoque
from llm_module.tools.sql_tools import tool_descobrir_tabelas

load_dotenv()
SYSTEM_PROMPT_LOCATION = os.getenv("SYSTEM_PROMPT_LOCATION")
MAX_INPUT_SIZE = int(os.getenv("MAX_INPUT_LENGTH", "4000"))

class chat_bot_service:
    def __init__(self):
        self.model = ChatOllama(model="qwen2.5:7B", temperature=0.0)
        self.middleware = []
        self.tools = [tool_get_current_time, tool_consultar_estoque, tool_calcular_validade, tool_descobrir_tabelas]
        self.prompt = SystemMessage(content=self._get_system_prompt())
        self.agent = self._build_agent()

    def _build_agent(self):
        
        agent = create_agent(
            model=self.model,
            middleware=self.middleware,
            tools=self.tools,
            system_prompt=self.prompt,
            checkpointer=None
        )
        
        return agent

    def _get_system_prompt(self) -> str:
        if not SYSTEM_PROMPT_LOCATION:
            raise ValueError("SYSTEM_PROMPT_LOCATION não definido")
        
        loader = TextLoader(SYSTEM_PROMPT_LOCATION, encoding='utf-8')
        docs = loader.load()
        return docs[0].page_content
    
    def _validate_user_input(self, user_input: str):
        """
        Responsavel por validar a entrada do usuario
        -> se é uma string
        -> se nao está vazia
        -> se é muito longa
        """
        if not isinstance(user_input, str):
            raise TypeError("Entrada deve ser uma string")
        
        content = user_input.strip()

        if not content:
            raise ValueError("Entrada vazia")
        
        if len(content) > MAX_INPUT_SIZE:
            raise RuntimeError("Entrada muito longa")

    async def send_message(self, 
                     user_input: str, 
                     session_id: str | None = None, 
                     user_id: str | None = None
                    ) -> dict:
        """
        Responsavel por enviar a entrada do usuario ao agente
        Identificando qual sessão e qual usuario estamos conversando
        Retorna um dicionario com a resposta e o id de sessao e usuario para identificacao
        """

        if not self.agent:
            raise RuntimeError("Agent nao inicializado")
        
        self._validate_user_input(user_input=user_input)
        
        result = await self.agent.ainvoke(
            {
                "messages": [HumanMessage(content=user_input)]
            },
            config={
                "metadata": {
                    "session_id": session_id,
                    "user_id": user_id
                }
            }
        )

        return result["messages"][-1].content

"""
Bloco de testes, um exemplo de como chamar a Minerva
"""

async def testes():
    chat = chat_bot_service()

    resp = await chat.send_message(
        "Verifique a movimentação de parafusos no estoque."
    )
    print("------------------------")
    print(resp[-1].content)
    print("------------------------")

    resp = await chat.send_message(
        "tem placas no sistema? quais são?"
    )
    print("------------------------")
    print(resp[-1].content)
    print("------------------------")
    
    resp = await chat.send_message(
        "Tem parafuso na tabela de produto? Se tem, que tipo de parafuso é?"
    )
    
    print("------------------------")
    print(resp[-1].content)
    print("------------------------")

if __name__ == "__main__":
    print("Iniciando testes...\n")
    import asyncio
    asyncio.run(testes())
    print("Testes finalizados.")

        
