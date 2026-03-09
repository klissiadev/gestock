class RouterService:

    REPORT_KEYWORDS = [
        "relatorio",
        "relatório",
        "inventario",
        "inventário",
        "curva abc",
        "movimentacao",
        "movimentação",
        "saldo de estoque",
        "giro de estoque",
    ]

    def decide(self, message: str) -> str:

        text = message.lower()

        if any(k in text for k in self.REPORT_KEYWORDS):
            return "report"

        return "chat"