import pandas as pd

class BatchDetector:

    def __init__(self, anomaly_service):
        self.service = anomaly_service

    def classify_result(self, score):
        if score < -0.30:
            return -1
        elif score < -0.10:
            return 0
        else:
            return 1

    def detect_dataframe(self, df):

        results = []

        for _, row in df.iterrows():

            result = self.service.detect(
                category=row["category"],
                store=row["store"],
                value=row["value"],
                sell_price=row["sell_price"],
                date=row["date"]
            )

            if result.get("status") == "model_not_found":
                continue

            allowed_fields = [
                "item_id",
                "nome",
                "descricao",
                "tipo",
                "estoque_minimo",
                "data_validade",
                "ativo",
                "cliente",
                "created_at",
                "quantidade",
                "preco_de_venda"
            ]

            row_result = {k: row[k] for k in allowed_fields if k in row}

            row_result.update({
                "anomaly": result["anomaly"],
                "score": result["score"],
                "result": min(result["anomaly"], self.classify_result(result["score"]))
            })

            results.append(row_result)

        if not results:
            return pd.DataFrame()

        return pd.DataFrame(results)