from llm_module.reports.report_repository import ReportRepository
from llm_module.reports.report_service import ReportService


def test_repository():
    print("\n=== TESTANDO REPOSITORY ===")

    repo = ReportRepository()

    dados = repo.get_estoque_baixo()

    print("Resultado repository:")
    print(dados)

    print("Total:", len(dados) if dados else 0)


def test_service():
    print("\n=== TESTANDO SERVICE ===")

    service = ReportService(ReportRepository())

    resultado = service.generate("estoque_baixo")

    print("Resultado service:")
    print(resultado)


if __name__ == "__main__":
    test_repository()
    test_service()
