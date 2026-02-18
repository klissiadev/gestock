from .base_formatter import BaseReportFormatter


class CurvaABCFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):

        metadata_text = metadata if metadata else ""

        return f"""
RELATÓRIO: Curva ABC de Produtos

PARÂMETROS:
{parametros}

METADADOS:
{metadata_text}

TOTAL DE PRODUTOS:
{total_items}

CLASSIFICAÇÃO:

{chr(10).join(registros_formatados)}
""".strip()
