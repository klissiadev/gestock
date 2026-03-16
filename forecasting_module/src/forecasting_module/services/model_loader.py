#carrega o modelo e os scalers para cada item_id a partir do arquivo .pkl
import joblib

class ModelRegistry:

    def __init__(self, model_path):

        data = joblib.load(model_path)
        
        print(f"DEBUG: Keys found in pickle: {data.keys() if isinstance(data, dict) else 'Not a dict'}")

        self.models = data["models"]
        self.scalers = data["scalers"]

    def get_model(self, item_id):

        model = self.models.get(item_id)
        scaler = self.scalers.get(item_id)

        return model, scaler