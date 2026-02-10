from langchain_ollama import ChatOllama

from llm_module.agents.report_agent import ReportAgent, ReportInput
from llm_module.reports.report_service import ReportService
from llm_module.reports.report_repository import ReportRepository


class ReportOrchestratorService:

    def __init__(self):

        self.report_service = ReportService(
            repository=ReportRepository()
        )

        self.report_agent = ReportAgent(
            model=ChatOllama(
                model="llama3.1:8b",
                temperature=0,
                top_p=0.1
            )
        )
        print("Modelo do report agent:", self.report_agent.model.model)
    async def gerar_relatorio(
        self,
        report_type: str,
        params: dict | None = None,
    ) -> str:

        params = params or {}

        print("ORCHESTRATOR RECEBEU:", report_type, params)

        try:

            # =============================
            # Busca dados estruturados
            # =============================
            resultado = self.report_service.generate(
                report_type=report_type,
                params=params,
            )

            # =============================
            # Validação de dados
            # =============================
            dados = resultado.get("data") or []

            if not isinstance(dados, list) or not dados:
                return "Não há informação disponível no sistema para responder a esta pergunta."

            # =============================
            # Monta input formal
            # =============================
            report_input = ReportInput(
                report_type=resultado["report_type"],
                tipo=resultado["title"],
                dados={
                    "registros": dados,
                    "metadata": resultado.get("metadata", {})
                },
                parametros=resultado.get("params", {}),
            )

            # =============================
            # Geração textual final
            # =============================
            return await self.report_agent.gerar(report_input)

        except ValueError as e:
            return str(e)

        except Exception as e:
            print("ERRO ORCHESTRATOR:", str(e))
            raise
