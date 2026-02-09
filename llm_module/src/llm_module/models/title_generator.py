from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio
import os

class TitleGenerator:
    def __init__(self):
        self.agent = create_agent(
            model=ChatOllama(model="gemma3:1b", temperature=0.5),
            system_prompt=SystemMessage(
                content=(
                    "Você receberá uma mensagem inicial do usuário. "
                    "Sua tarefa é criar um título curto e coerente para a conversa, "
                    "com no máximo 24 caracteres (incluindo espaços), em português. "
                    "O título deve ser um resumo do tema da conversa. "
                    "IMPORTANTE: Responda SOMENTE com o título, sem explicações adicionais, "
                    "sem emojis e sem frases completas. "
                    "Se não houver contexto suficiente, responda apenas com 'Conversa'."
                    "\n\nExemplos:\n"
                    "Usuário: \"me diz como está o estoque\"\n"
                    "Título: Controle de estoque\n\n"
                    "Usuário: \"preciso de ajuda com vendas\"\n"
                    "Título: Suporte em vendas\n\n"
                    "Usuário: \"Quais dados posso consultar?\"\n"
                    "Título: Consulta de dados\n"
                    "IMPORTANTE: Sua resposta deve conter APENAS o título, sem explicações, sem frases completas, sem emojis. Se não houver contexto suficiente, responda a mensagem com no máiximo 24 caracteres."
                )
            )
        )
        
    async def send_message(self, user_input: str):
        if not self.agent:
            raise RuntimeError("Serviço não inicializado")
        
        result = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=f"""{user_input}""")]},)
        
        # Dependendo da versão, pode ser AIMessage ou dict
        if "messages" in result:
            bot_response = result["messages"][-1].content
        else:
            bot_response = result.content
        
        return bot_response
    

async def main():
    chat = TitleGenerator()
    test_inputs = [
        "Quais dados posso consultar?",
        "Tenho um erro no processo",
        "Olá Minerva, me ajude na tela de solicitações.",
        "Olá Minerva, me ajude na tela inicial.",
        "Olá Minerva, me ajude com o estoque.",
        "Testando, você conhece o Rayan",
        "Você conhece o Club de Regatas Vasco da Gama",
        "Gere um relatório de estoque baixo",
        "Gere um relatório da curva abc",
        "Faça a geração de relatório de inventario",
        "Faça a geração de relatório de giro de estoque",
        "Meu nome é Júlia, pode me ajudar a consultar o estoque?",
        "quants placas tem no estoque",
        "oi diva, o que voce pode fazer por mim hj?",
        "bom dia, pode me falar sobre o clima?",
        "aaah, então quais produtos estão ativos no estoque?",
        "existe itens com estoque negativo?",
        "opa, meu nome é luiza. o que voce pode fazer por mim hj?",
        "pode me mostrar movimentações recentes",
        "me diz como ta o estoque",
        "nao entendi muito bem, pode explicar direitinho?",
        "aaaah, vc pode gerar relatórios?",
        "oi"
    ]

    # Executa os testes
    for phrase in test_inputs:
        response = await chat.send_message(phrase)
        print(f"Usuário: {phrase}\nTítulo: {response}\n{'-'*40}")


if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot desligado pelo usuário.")