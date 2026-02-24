from .base_formatter import BaseReportFormatter


class ValidadeProximaFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        return f"""
RELATÓRIO: Produtos com Validade Próxima

PARÂMETROS:
{parametros}

TOTAL DE ITENS:
{total_items}

LISTAGEM:

{chr(10).join(registros_formatados)}
""".strip()
