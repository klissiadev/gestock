# llm_module/src/llm_module/services/router_service.py
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
import logging

logger = logging.getLogger(__name__)

class IntentRouterService:
    def __init__(self):
        self.classifier_model = ChatOllama(model="gemma3:270m", temperature=0.0)
        
        self.system_prompt = """
        Você é um classificador de intenções estrito. Sua única função é ler a mensagem do usuário e responder com EXATAMENTE UMA das duas palavras abaixo, sem explicações:
        
        RELATORIO - Se o usuário estiver pedindo balanços, relatórios, consolidações gerais, curva ABC, giro de estoque, inventário, ou análises agregadas. Ex: "Me dê um balanço do estoque", "Qual a curva ABC?", "Relatório de validade".
        GERAL - Se o usuário estiver fazendo perguntas do dia a dia, buscando um produto específico, buscando uma movimentação, dúvidas ou qualquer outra coisa. Ex: "Onde está o produto X?", "Quais as movimentações de ontem?", "Olá, tudo bem?".
        """

    async def classify_intent(self, user_message: str) -> str:
        try:
            resposta = await self.classifier_model.ainvoke([
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_message)
            ])
            
            intent = resposta.content.strip().upper()
            
            if "RELATORIO" in intent:
                return "RELATORIO"
            return "GERAL"
        except Exception as e:
            logger.error(f"Erro na classificação de intenção, caindo para GERAL: {e}")
            return "GERAL" 