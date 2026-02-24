def detect_report(message: str) -> dict | None:
    msg = message.lower()

    if "estoque" in msg:
        return {
            "report_type": "estoque_baixo",
            "params": {}
        }

    if "sem giro" in msg:
        return {
            "report_type": "produtos_sem_giro",
            "params": {"dias": 30}
        }

    if "validade" in msg:
        return {
            "report_type": "validade_proxima",
            "params": {"dias": 30}
        }

    return None