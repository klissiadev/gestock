# llm_module/src/llm_module/services/router_service.py
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
import logging

logger = logging.getLogger(__name__)

class IntentClassifier:
    def __init__(self):
        self.classifier_model = ChatOllama(model="gemma3:270m", temperature=0.0)
        
        self.system_prompt = """Você é um classificador de intenções estrito. Sua única função é ler a mensagem do usuário e responder com EXATAMENTE UMA das duas palavras abaixo, sem explicações:
        
        RELATORIO - Se o usuário pedir a geração de análises agregadas, balanços, consolidações ou RELATÓRIOS. É obrigatório classificar como RELATORIO se a mensagem envolver qualquer um dos seguintes temas:
        - estoque baixo
        - produtos sem giro
        - movimentação por período
        - entradas e saídas
        - validade próxima
        - inventário
        - saldo de estoque
        - giro de estoque
        - curva abc
        - produtos por custo (ou custo de produtos)
        Exemplos de RELATORIO: "Faça a geração de relatório de estoque baixo", "Qual a curva ABC?", "Relatório de validade", "Gere um inventário".
        
        GERAL - Se o usuário estiver fazendo perguntas do dia a dia, buscando informações de UM produto específico, dúvidas operacionais ou bate-papo. 
        Exemplos de GERAL: "Onde está o produto X?", "Quais as movimentações de ontem do item Y?", "Olá, tudo bem?"
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