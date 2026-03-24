from .inventario_formatter import InventarioFormatter
from .estoque_baixo_formatter import EstoqueBaixoFormatter
from .saldo_estoque_formatter import SaldoEstoqueFormatter
from .movimentacao_periodo_formatter import MovimentacaoPeriodoFormatter
from .entradas_saidas_formatter import EntradasSaidasFormatter
from .produtos_sem_giro_formatter import ProdutosSemGiroFormatter
from .validade_proxima_formatter import ValidadeProximaFormatter
from .giro_estoque_formatter import GiroEstoqueFormatter
from .curva_abc_formatter import CurvaABCFormatter
from .produtos_custo_formatter import ProdutosCustoFormatter


FORMATTERS = {
    "inventario": InventarioFormatter(),
    "estoque_baixo": EstoqueBaixoFormatter(),
    "saldo_estoque": SaldoEstoqueFormatter(),
    "movimentacao_periodo": MovimentacaoPeriodoFormatter(),
    "entradas_saidas": EntradasSaidasFormatter(),
    "produtos_sem_giro": ProdutosSemGiroFormatter(),
    "validade_proxima": ValidadeProximaFormatter(),
    "giro_estoque": GiroEstoqueFormatter(),
    "curva_abc": CurvaABCFormatter(),
    "produtos_custo": ProdutosCustoFormatter(),
}