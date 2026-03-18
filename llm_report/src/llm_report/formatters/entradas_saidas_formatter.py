from .base_formatter import BaseReportFormatter


class EntradasSaidasFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        return f"""
RELATÓRIO: Movimentação de Produtos – Entradas e Saídas

PERÍODO ANALISADO:
{parametros}

TOTAL DE PRODUTOS ANALISADOS:
{total_items}

RESUMO EXECUTIVO:
- Este relatório apresenta as movimentações consolidadas de produtos no período informado.
- Os dados já foram previamente organizados pelo sistema.

DETALHAMENTO POR PRODUTO:

{chr(10).join(registros_formatados)}
""".strip()
