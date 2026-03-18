from .base_formatter import BaseReportFormatter


class MovimentacaoPeriodoFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        return f"""
RELATÓRIO: Movimentações de Estoque

PERÍODO ANALISADO:
{parametros}

TOTAL DE MOVIMENTAÇÕES:
{total_items}

MOVIMENTAÇÕES:

{chr(10).join(registros_formatados)}
""".strip()
