class BaseReportFormatter:

    def montar_relatorio(
        self,
        registros_formatados: list[str],
        parametros: str,
        total_items: int,
        metadata: dict | None = None
    ) -> str:
        raise NotImplementedError
