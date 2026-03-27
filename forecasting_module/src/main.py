from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from forecasting_module.services.model_loader import ModelRegistry
from forecasting_module.services.anomaly_service import AnomalyService
from forecasting_module.services.batch_detector import BatchDetector
from forecasting_module.services.anomaly_app_service import AnomalyAppService
from forecasting_module.api.anomaly_router import create_anomaly_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "forecasting_module/ml_artifacts/modelos_vendas_completo.pkl"

registry = ModelRegistry(MODEL_PATH)
service = AnomalyService(registry)
detector = BatchDetector(service)
app_service = AnomalyAppService(detector)

app.include_router(create_anomaly_router(app_service))
