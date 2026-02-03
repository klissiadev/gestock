from langchain_ollama import ChatOllama
from llm_module.agents.report_agent import ReportAgent, ReportInput
from reports.report_service import ReportService
from reports.report_repository import ReportRepository


class ReportOrchestratorService:
    def __init__(self):
        self.report_service = ReportService(
            repository=ReportRepository()
        )

        self.report_agent = ReportAgent(
            model=ChatOllama(model="qwen2.5:7B", temperature=0.0)
        )

    async def gerar_relatorio(
        self,
        report_type: str,
        params: dict | None = None,
    ) -> str:
        #Busca dados estruturados (SEM LLM)
        resultado = self.report_service.generate(
            report_type=report_type,
            params=params,
        )

        #Monta input formal para o agente
        report_input = ReportInput(
            tipo=resultado["title"],
            dados=resultado["data"],
            parametros=resultado["params"],
        )

        #Geração textual final
        return await self.report_agent.gerar(report_input)
