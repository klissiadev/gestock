from .base_formatter import BaseReportFormatter


class GiroEstoqueFormatter(BaseReportFormatter):

    def montar_relatorio(self, registros_formatados, parametros, total_items, metadata=None):
        payload = {
            "total_items": total_items,
            "parametros": parametros,
            "dados": registros_formatados
        }

        return self.wrap_json(
            report_type="giro_estoque",
            payload=payload,
            metadata=metadata
        )
