from .base_formatter import BaseReportFormatter


class ProdutosCustoFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):
        payload = {
            "total_items": total_items,
            "parametros": parametros,
            "dados": registros_formatados
        }

        return self.wrap_json(
            report_type="produtos_custo",
            payload=payload,
            metadata=metadata
        )
