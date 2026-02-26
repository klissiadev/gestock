from .base_formatter import BaseReportFormatter


class SaldoEstoqueFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        return f"""
RELATÓRIO: Saldo Atual de Estoque

PARÂMETROS:
{parametros}

TOTAL DE REGISTROS:
{total_items}

LISTAGEM:

{chr(10).join(registros_formatados)}
""".strip()
