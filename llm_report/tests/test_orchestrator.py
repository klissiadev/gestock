import asyncio
from llm_module.services.report_orchestrator import ReportOrchestratorService


async def main():
    orchestrator = ReportOrchestratorService()

    resposta = await orchestrator.gerar_relatorio("giro_estoque")

    print("\n===== RESULTADO =====")
    print(resposta)


if __name__ == "__main__":
    asyncio.run(main())
