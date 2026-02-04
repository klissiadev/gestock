from langchain.tools import tool

from reports.report_service import ReportService
from reports.report_repository import ReportRepository
from llm_module.agents.report_agent import ReportAgent

repository = ReportRepository()
report_service = ReportService(repository)
report_agent = ReportAgent()


@tool
async def gerar_relatorio(tipo: str, params: dict | None = None) -> dict:
    """
    Gera relatórios oficiais do sistema.

    Tipos válidos:
    - estoque_baixo
    - produtos_sem_giro
    - movimentacao_periodo
    - entradas_saidas
    - validade_proxima
    """
    params = params or {}

    try:
        report_data = report_service.generate(
            report_type=tipo,
            params=params
        )

        texto = await report_agent.gerar({
            "tipo": report_data["report_type"],
            "parametros": report_data["params"],
            "dados": report_data
        })

        return {
            "kind": "report",
            "title": report_data["title"],
            "content": texto,
            "generated_at": report_data["generated_at"]
        }

    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Erro inesperado ao gerar relatório",
            "details": str(e)
        }