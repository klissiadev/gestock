from enum import Enum
from typing import Any, Dict, List, Callable
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from llm_module.builders.analysis_builder import AnalysisBuilder
from llm_module.builders.movement_builder import MovementBuilder
from llm_module.reports.report_repository import ReportRepository
from llm_module.utils.llm_normalizer import normalize_llm_data


class ReportType(Enum):
    ESTOQUE_BAIXO = "estoque_baixo"
    PRODUTOS_SEM_GIRO = "produtos_sem_giro"
    MOVIMENTACAO_PERIODO = "movimentacao_periodo"
    ENTRADAS_SAIDAS = "entradas_saidas"
    VALIDADE_PROXIMA = "validade_proxima"

    INVENTARIO = "inventario"
    SALDO_ESTOQUE = "saldo_estoque"
    GIRO_ESTOQUE = "giro_estoque"
    CURVA_ABC = "curva_abc"
    PRODUTOS_CUSTO = "produtos_custo"


class ReportService:
    """
    Responsável por:

    - Validar parâmetros
    - Selecionar consulta
    - Aplicar cálculos analíticos
    - Retornar dados estruturados
    """

    def __init__(self, repository: ReportRepository):
        self.repository = repository

        self._handlers: Dict[ReportType, Callable] = {
            ReportType.ESTOQUE_BAIXO: self._estoque_baixo,
            ReportType.PRODUTOS_SEM_GIRO: self._produtos_sem_giro,
            ReportType.MOVIMENTACAO_PERIODO: self._movimentacao_periodo,
            ReportType.ENTRADAS_SAIDAS: self._entradas_saidas,
            ReportType.VALIDADE_PROXIMA: self._validade_proxima,
            ReportType.INVENTARIO: self._inventario,
            ReportType.SALDO_ESTOQUE: self._saldo_estoque,
            ReportType.GIRO_ESTOQUE: self._giro_estoque,
            ReportType.CURVA_ABC: self._curva_abc,
            ReportType.PRODUTOS_CUSTO: self._produtos_custo,
        }

    # --------------------------------------------------
    # ENTRYPOINT
    # --------------------------------------------------

    def generate(
        self,
        report_type: str,
        params: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:

        try:
            report_enum = ReportType(report_type)
        except ValueError:
            raise ValueError(f"Tipo de relatório inválido: {report_type}")

        params = params or {}

        handler = self._handlers.get(report_enum)

        if not handler:
            raise ValueError(f"Relatório não suportado: {report_type}")

        data, metadata, title = handler(params)

        return self._build_response(
            report_enum,
            title,
            data,
            params,
            metadata
        )

    # --------------------------------------------------
    # RESPONSE BUILDER
    # --------------------------------------------------

    def _build_response(
        self,
        report_enum: ReportType,
        title: str,
        data: Any,
        params: Dict[str, Any],
        metadata: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:

        return {
            "kind": "report",
            "report_type": report_enum.value,
            "title": title,
            "generated_at": datetime.utcnow().isoformat(),
            "params": params,
            "metadata": metadata or {},
            "total_items": len(data["registros"]) if isinstance(data, dict) else len(data),
            "data": data,
        }

    # --------------------------------------------------
    # estoque_baixo
    # --------------------------------------------------

    def _estoque_baixo(self, params):
        limite = params.get("limite")
        data = self.repository.get_estoque_baixo(limite)

        return data, {}, "Produtos com estoque abaixo do mínimo"
    
    # --------------------------------------------------
    # produtos_sem_giro
    # --------------------------------------------------

    def _produtos_sem_giro(self, params):

        if "data_limite" in params:
            data_limite = date.fromisoformat(params["data_limite"])
        else:
            dias = max(self._safe_int(params.get("dias"), 30), 0)
            data_limite = date.today() - timedelta(days=dias)

        data = self.repository.get_produtos_sem_giro(data_limite)

        return data, {"data_limite": data_limite.isoformat()}, "Produtos sem giro"



    # --------------------------------------------------
    # movimentacao_periodo
    # --------------------------------------------------

    def _movimentacao_periodo(self, params):

        data_inicio, data_fim = self._validate_period(params)

        registros = self.repository.get_movimentacao_periodo(
            data_inicio, data_fim
        )

        metadata = {
            "data_inicio": data_inicio,
            "data_fim": data_fim
        }

        return registros, metadata, "Movimentações no período"
    # --------------------------------------------------
    # Entradas_saida
    # --------------------------------------------------
    def get_movimentacoes_agrupadas(self, params):

        data_inicio, data_fim = self._validate_period(params)

        registros = self.repository.get_entradas_saidas(
            data_inicio, data_fim
        )

        return MovementBuilder.agrupar_entradas_saidas(registros)

    def _entradas_saidas(self, params):

        data_inicio, data_fim = self._validate_period(params)

        registros = self.repository.get_entradas_saidas(
            data_inicio, data_fim
        )

        dados_agrupados = MovementBuilder.agrupar_entradas_saidas(registros)

        metadata = {
            "data_inicio": data_inicio,
            "data_fim": data_fim
        }

        return dados_agrupados, metadata, "Resumo de entradas e saídas"
    
    # --------------------------------------------------
    # valdiade_proxima
    # --------------------------------------------------


    def _validade_proxima(self, params):

        if "data_limite" in params:
            data_limite = date.fromisoformat(params["data_limite"])
            dias = max((data_limite - date.today()).days, 0)
        else:
            dias = max(self._safe_int(params.get("dias"), 30), 0)

        data = self.repository.get_validade_proxima(dias)

        return data, {"dias_analisados": dias}, "Produtos com validade próxima"

    # --------------------------------------------------
    # NOVOS RELATÓRIOS
    # --------------------------------------------------

    def _inventario(self, params):
        data = self.repository.get_inventario()

        return data, {}, "Relatório de Inventário"

    def _saldo_estoque(self, params):
        data = self.repository.get_saldo_estoque()

        return data, {}, "Saldo Atual de Estoque"

    def _giro_estoque(self, params):
        data = self.repository.get_giro_estoque()

        return data, {}, "Giro de Estoque"

    def _curva_abc(self, params):
        produtos = self.repository.get_produtos_custo()

        if not produtos:
            return [], {}, "Curva ABC"

        total_valor = sum(p["valor_total"] for p in produtos)

        if total_valor == 0:
            return [], {"valor_total_estoque": 0}, "Relatório Curva ABC"

        acumulado = Decimal("0")
        resultado = []

        produtos_ordenados = sorted(
            produtos,
            key=lambda x: x["valor_total"],
            reverse=True
        )

        for p in produtos_ordenados:
            percentual = p["valor_total"] / total_valor
            acumulado += percentual

            percentual_formatado = (percentual * 100).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            if acumulado <= Decimal("0.8"):
                classe = "A"
            elif acumulado <= Decimal("0.95"):
                classe = "B"
            else:
                classe = "C"

            resultado.append({
                **p,
                "percentual": percentual_formatado,
                "classe_abc": classe
            })

        metadata = {"valor_total_estoque": total_valor}

        return resultado, metadata, "Relatório Curva ABC"
    
    # --------------------------------------------------
    # produtos_custo
    # --------------------------------------------------
    def _produtos_custo(self, params):
        data = self.repository.get_produtos_custo()
        data = normalize_llm_data(data)

        return data, {}, "Produtos e Seus Custos"

    # --------------------------------------------------
    # VALIDADORES
    # --------------------------------------------------

    from datetime import datetime


    def _safe_int(self, value, default):
        try:
            return int(value)
        except Exception:
            return default


    def _validate_period(self, params):

        data_inicio = params.get("data_inicio")
        data_fim = params.get("data_fim")

        if not data_inicio or not data_fim:
            raise ValueError("data_inicio e data_fim são obrigatórios")

        try:
            datetime.fromisoformat(data_inicio)
            datetime.fromisoformat(data_fim)
        except Exception:
            raise ValueError("Datas devem estar no formato YYYY-MM-DD")

        return data_inicio, data_fim
