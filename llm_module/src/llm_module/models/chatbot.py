from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import SystemMessage
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import os, time, uuid

from llm_module.tools.sql_tools import (
    tool_listar_produtos,
    tool_produtos_vencendo,
    tool_produtos_vencimento_proximo,
    tool_contagem_produtos,
)

load_dotenv()
SYSTEM_PROMPT_LOCATION = os.getenv("SYSTEM_PROMPT_LOCATION")
MAX_INPUT_SIZE = int(os.getenv("MAX_INPUT_LENGTH", "4000"))

class chat_bot_service:
    def __init__(self):
        self.model = ChatOllama(model="llama3.2:3b", temperature=0.7)
        self.middleware = []
        self.tools = [
            tool_listar_produtos,
            tool_produtos_vencendo,
            tool_produtos_vencimento_proximo,
            tool_contagem_produtos,
        ]
        self.prompt = SystemMessage(content=self._get_system_prompt())
        self.agent = self._build_agent()

    def _build_agent(self,
                    session_id: str | None = None, 
                    user_id: str | None = None
                    ):
        """
        Responsavel pela construcao do agente
        -> retorna agente com seu prompt inicializado
        -> checkpoints de memoria determinados
        -> ferramentas atribuidas 
        
        TO DO: 
        - adicionar ferramentas
        - adicionar middleware
        - adicionar memoria (por isso variaveis de id_Sessao e id_usuario)
        """ 
        return create_agent(
            model=self.model,
            middleware=self.middleware,
            tools=self.tools,
            system_prompt=self.prompt,
            checkpointer=None
        )

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

    def send_message(self, 
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
        
        result = self.agent.invoke(
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
    As funcoes a seguir precisam da existencia de uma tela de usuario para funcionar... vish
    """
    
    def start_session(self, user_id: str | None = None):
        pass

    def end_session(self, session_id: str | None = None):
        pass

    def get_history(self, session_id: str | None = None):
        """
            Busca o histórico de conserva de uma respectiva sessao
        """
        pass

    def clear_history(self, session_id: str | None = None):
        """
            Limpa o historico de conversa (que o assistente ira se lembrar na hora de conversar)
        """
        pass


# Testes
chat = chat_bot_service()
# print(chat.send_message("Quantos produtos temos no estoque?"))
# print(" ")
print(chat.send_message("Liste os produtos que estão para vencer nos próximos 15 dias."))
print(" ")
print(chat.send_message("Liste os produtos que estão para vencer nos próximos 2000 dias."))
print(" ")

# print(chat.send_message("Me liste todos os produtos cadastrados no sistema."))
# print(" ")
# print(chat.send_message("Qual produto vai vencer primeiro?"))
# print(" ")
        
