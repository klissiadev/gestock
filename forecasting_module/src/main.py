from forecasting_module.core.data_loader import load_database
from forecasting_module.services.batch_detector import BatchDetector
from forecasting_module.services.model_loader import ModelRegistry


# Ficaria na pasta ml_artifacs
MODEL_PATH = "src\\forecasting_module\\ml_artifacts\\modelos_vendas_completo.pkl"


def main():
    registry = ModelRegistry(MODEL_PATH)
    detector = BatchDetector(registry)

    # Todas as movimentações de saida do produto id 32 nos ultimmos 30 dias formatados em dataframe
    df = load_database(produto_id=32, tft_days=30)

    resultado = detector.detect_dataframe(df)

    print(resultado.head())

if __name__ == "__main__":
    main()