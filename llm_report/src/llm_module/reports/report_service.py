from enum import Enum
from typing import Any, Dict, List
from datetime import datetime

from reports.report_repository import ReportRepository


class ReportType(Enum):
    ESTOQUE_BAIXO = "estoque_baixo"
    PRODUTOS_SEM_GIRO = "produtos_sem_giro"
    MOVIMENTACAO_PERIODO = "movimentacao_periodo"
    ENTRADAS_SAIDAS = "entradas_saidas"
    VALIDADE_PROXIMA = "validade_proxima"


class ReportService:
    """
    Camada responsável por orquestrar a geração de relatórios.
    - Decide qual consulta executar
    - Valida parâmetros
    - Retorna dados estruturados (sem linguagem natural)
    """

    def __init__(self, repository: ReportRepository):
        self.repository = repository

    def generate(self, report_type: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        try:
            report_enum = ReportType(report_type)
        except ValueError:
            raise ValueError(f"Tipo de relatório inválido: {report_type}")

        params = params or {}

        if report_enum == ReportType.ESTOQUE_BAIXO:
            data = self._estoque_baixo(params)
            title = "Produtos com estoque abaixo do mínimo"

        elif report_enum == ReportType.PRODUTOS_SEM_GIRO:
            data = self._produtos_sem_giro(params)
            title = "Produtos sem giro"

        elif report_enum == ReportType.MOVIMENTACAO_PERIODO:
            data = self._movimentacao_periodo(params)
            title = "Movimentações no período"

        elif report_enum == ReportType.ENTRADAS_SAIDAS:
            data = self._entradas_saidas(params)
            title = "Resumo de entradas e saídas"

        elif report_enum == ReportType.VALIDADE_PROXIMA:
            data = self._validade_proxima(params)
            title = "Produtos com validade próxima"

        else:
            raise ValueError(f"Tipo de relatório não suportado: {report_type}")

        return {
            "kind": "report",
            "report_type": report_enum.value,
            "title": title,
            "generated_at": datetime.utcnow().isoformat(),
            "params": params,
            "total_items": len(data) if isinstance(data, list) else None,
            "data": data,
        }


    # -------------------------
    # Relatórios individuais
    # -------------------------

    def _estoque_baixo(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        limite = params.get("limite")
        return self.repository.get_estoque_baixo(limite)

    def _produtos_sem_giro(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        dias = params.get("dias", 30)
        return self.repository.get_produtos_sem_giro(dias)

    def _movimentacao_periodo(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        data_inicio = params.get("data_inicio")
        data_fim = params.get("data_fim")

        if not data_inicio or not data_fim:
            raise ValueError("data_inicio e data_fim são obrigatórios")

        return self.repository.get_movimentacao_periodo(data_inicio, data_fim)

    def _entradas_saidas(self, params: Dict[str, Any]) -> Dict[str, Any]:
        data_inicio = params.get("data_inicio")
        data_fim = params.get("data_fim")

        if not data_inicio or not data_fim:
            raise ValueError("data_inicio e data_fim são obrigatórios")

        return self.repository.get_entradas_saidas(data_inicio, data_fim)

    def _validade_proxima(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        dias = params.get("dias", 30)
        return self.repository.get_validade_proxima(dias)
