from langchain.tools import tool
from reports.report_service import ReportService
from reports.report_repository import ReportRepository

repository = ReportRepository()
report_service = ReportService(repository)

@tool
def gerar_relatorio(tipo: str, params: dict | None = None) -> dict:
    """
    Gera relatórios de estoque e movimentações.

    Tipos suportados:
    - estoque_baixo
    - validade_proxima
    - produtos_sem_giro
    - movimentacao_periodo
    - entradas_saidas

    params: dicionário com parâmetros específicos de cada relatório.
    Ex:
      {"dias": 30}
      {"data_inicio": "2025-01-01", "data_fim": "2025-01-31"}
    """
    if params is None:
        params = {}

    try:
        return report_service.generate(tipo=tipo, params=params)
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
