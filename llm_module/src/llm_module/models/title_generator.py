from langchain_ollama import ChatOllama

class TitleGeneratorService:
    def __init__(self):
        self.summary_model = ChatOllama(model="gemma3:270m", temperature=0.0)
        self.prompt = None


    async def generate_title(self, text: str) -> str:
        """Gera um título curto e objetivo para a sessão."""
        prompt = (
            "Você é um assistente de indexação. Resuma a intenção do usuário em um título de 2 a 4 palavras.\n"
            "Regras: Responda APENAS o título. Sem pontuação. Sem explicações.\n\n"
            f"Entrada: '{text[:300]}'\n"
            "Título:"
        )
        try:
            res = await self.summary_model.ainvoke(prompt)
            title = res.content.strip().split('\n')[0].replace('"', '').replace('.', '')
            return title if len(title) > 2 else "Nova Conversa"

        except Exception as e:
            return "Nova Conversa"