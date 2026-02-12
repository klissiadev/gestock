import asyncio
from llm_module.services.report_orchestrator import ReportOrchestratorService


async def main():
    orchestrator = ReportOrchestratorService()

    """resposta = await orchestrator.gerar_relatorio(
        "entradas_saidas",
        {
            "data_inicio": "2024-01-01",
            "data_fim": "2026-12-31"
        }
    )"""

    resposta = await orchestrator.gerar_relatorio(
        "estoque_baixo"
    )

    """resposta = await orchestrator.gerar_relatorio("estoque_baixo")"""

    print("\n===== RESULTADO =====")
    print(resposta)


if __name__ == "__main__":
    asyncio.run(main())
