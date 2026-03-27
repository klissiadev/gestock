from ml.model_loader import ModelRegistry
from ml.batch_detector import BatchDetector
from database.db_loader import carregar_dados #a parte que pega os dados vindo do banco

MODEL_PATH = "models/modelo_isolation_forest.pkl"

def main():

    registry = ModelRegistry(MODEL_PATH)

    detector = BatchDetector(registry)

    df = carregar_dados()

    resultado = detector.detect_dataframe(df)

    print(resultado.head())

if __name__ == "__main__":
    main()