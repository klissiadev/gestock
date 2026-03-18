from .base_formatter import BaseReportFormatter


class InventarioFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        return f"""
RELATÓRIO: Inventário Completo

PARÂMETROS:
{parametros}

TOTAL DE PRODUTOS:
{total_items}

LISTAGEM:

{chr(10).join(registros_formatados)}
""".strip()
