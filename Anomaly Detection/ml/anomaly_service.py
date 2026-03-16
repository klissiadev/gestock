class AnomalyService:

    def __init__(self, model_registry):
        self.registry = model_registry

    def detect(self, item_id, value, sell_price):

        model, scaler = self.registry.get_model(item_id)

        if model is None:
            return {
                "item_id": item_id,
                "status": "model_not_found"
            }

        X = [[value, sell_price]]

        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[0]
        score = model.decision_function(X_scaled)[0]

        return {
            "item_id": item_id,
            "anomaly": int(prediction),
            "score": float(score)
        }