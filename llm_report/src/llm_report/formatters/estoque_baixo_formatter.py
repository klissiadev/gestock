from .base_formatter import BaseReportFormatter


class EstoqueBaixoFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        return f"""
RELATÓRIO: Produtos com Estoque Abaixo do Mínimo

PARÂMETROS UTILIZADOS:
{parametros}

TOTAL DE ITENS:
{total_items}

LISTAGEM:

{chr(10).join(registros_formatados)}
""".strip()
