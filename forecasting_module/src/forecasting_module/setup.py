# forecasting_module/src/forecasting_module/setup.py
from pathlib import Path
from fastapi import APIRouter
from forecasting_module.services.model_loader import ModelRegistry
from forecasting_module.services.anomaly_service import AnomalyService
from forecasting_module.services.batch_detector import BatchDetector
from forecasting_module.services.anomaly_app_service import AnomalyAppService
from forecasting_module.api.anomaly_router import create_anomaly_router

def get_forecasting_router(model_path: str = None) -> APIRouter:
    """
    Inicializa todas as dependências do módulo de forecast e retorna o APIRouter.
    """
    if not model_path:
        BASE_DIR = Path(__file__).resolve().parent
        CAMINHO_DO_MODELO = BASE_DIR / "ml_artifacts" / "modelos_vendas_completo.pkl"
        model_path = CAMINHO_DO_MODELO

    registry = ModelRegistry(model_path)
    service = AnomalyService(registry)
    detector = BatchDetector(service)
    app_service = AnomalyAppService(detector)

    router = create_anomaly_router(app_service)
    
    return router