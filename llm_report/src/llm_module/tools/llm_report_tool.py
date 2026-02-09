from langchain.tools import tool

from llm_module.services.report_orchestrator import ReportOrchestratorService

orchestrator = ReportOrchestratorService()

@tool(return_direct=True)
async def gerar_relatorio(tipo: str, parametros: dict | None = None) -> str:

    parametros = parametros or {}

    print(f"[TOOL] Gerando relatório: {tipo} | Params: {parametros}")

    try:
        return await orchestrator.gerar_relatorio(tipo, parametros)

    except Exception as e:
        print("Erro TOOL:", e)
        return "Erro ao gerar relatório."

