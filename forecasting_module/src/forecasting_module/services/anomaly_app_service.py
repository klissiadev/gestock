from forecasting_module.core.data_loader import load_anomaly_data

class AnomalyAppService:

    def __init__(self, detector):
        self.detector = detector

    def get_anomalies(self, data_corte):
        df = load_anomaly_data(data_corte)

        resultado = self.detector.detect_dataframe(df)

        if resultado.empty:
            return {
                "data": [],
                "count": 0
            }

        resultado["date"] = resultado["date"].astype(str)

        return {
            "data": resultado.to_dict(orient="records"),
            "count": len(resultado)
        }