import pandas as pd

class AnomalyService:

    def __init__(self, model_registry):
        self.registry = model_registry

    def detect(self, category, store, value, sell_price, date):

        model, scaler = self.registry.get_model((category, store))

        if model is None:
            return {
                "category": category,
                "store": store,
                "status": "model_not_found"
            }

        day_of_week = pd.to_datetime(date).dayofweek

        X = pd.DataFrame([{
                            "value": value,
                            "sell_price": sell_price,
                            "day_of_week": day_of_week
                        }])

        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[0]
        score = model.decision_function(X_scaled)[0]

        return {
            "category": category,
            "store": store,
            "anomaly": int(prediction),
            "score": float(score)
        }