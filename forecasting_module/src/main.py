from forecasting_module.core.data_loader import load_anomaly_data
from forecasting_module.services.batch_detector import BatchDetector
from forecasting_module.services.model_loader import ModelRegistry
from forecasting_module.services.anomaly_service import AnomalyService
from datetime import datetime

MODEL_PATH = "forecasting_module/ml_artifacts/modelos_vendas_completo.pkl"

def main():
    registry = ModelRegistry(MODEL_PATH)
    service = AnomalyService(registry)
    detector = BatchDetector(service)

    data_corte = datetime.strptime("01/01/2025", "%d/%m/%Y").date()

    df = load_anomaly_data(data_corte)

    print("Colunas:", df.columns.tolist())
    print(df.head())

    resultado = detector.detect_dataframe(df)

    print("\nResultado:")
    print(resultado)

if __name__ == "__main__":
    main()