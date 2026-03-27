from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

def create_anomaly_router(app_service):

    @router.get("/anomalies")
    def get_anomalies(data_corte: str):
        data_corte_parsed = datetime.strptime(data_corte, "%Y-%m-%d").date()

        return app_service.get_anomalies(data_corte_parsed)

    return router