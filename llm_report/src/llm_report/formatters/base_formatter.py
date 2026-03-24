import json

class BaseReportFormatter:
    
    def wrap_json(self, report_type, payload, metadata=None):
        """Cria o envelope padronizado para o frontend"""
        return json.dumps({
            "type": "REPORT_ACTION",
            "report_type": report_type,
            "payload": payload,
            "metadata": metadata or {}
        }, ensure_ascii=False)

    def montar_relatorio(
        self,
        registros_formatados: list[str],
        parametros: str,
        total_items: int,
        metadata: dict | None = None
    ) -> str:
        raise NotImplementedError
