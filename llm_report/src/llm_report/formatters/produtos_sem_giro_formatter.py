from .base_formatter import BaseReportFormatter


class ProdutosSemGiroFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        return f"""
RELATÓRIO: Produtos Sem Giro

PARÂMETROS:
{parametros}

TOTAL DE PRODUTOS:
{total_items}

LISTAGEM:

{chr(10).join(registros_formatados)}
""".strip()
