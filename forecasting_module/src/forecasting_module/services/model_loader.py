import joblib

class ModelRegistry:

    def __init__(self, model_path):
        self.models = joblib.load(model_path)

    def get_model(self, key):

        data = self.models.get(key)

        if data is None:
            return None, None

        return data["model"], data["scaler"]