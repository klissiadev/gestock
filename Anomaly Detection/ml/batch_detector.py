import pandas as pd

class BatchDetector:

    def __init__(self, registry):
        self.registry = registry

    def classify_result(self, score):

        if score < -0.30:
            return -1      # anomalia

        elif score < -0.10:
            return 0       # suspeito

        else:
            return 1       # normal
        
    def detect_dataframe(self, df):

        results = []

        for item_id, group in df.groupby("item_id"):

            model, scaler = self.registry.get_model(item_id)

            if model is None:
                continue

            X = group[["value", "sell_price"]]

            X_scaled = scaler.transform(X)

            group = group.copy()
            group["anomaly"] = model.predict(X_scaled)
            group["score"] = model.decision_function(X_scaled)

            group["result"] = group["score"].apply(self.classify_result)

            results.append(group)
        
        if not results:
            return pd.DataFrame()

        return pd.concat(results)