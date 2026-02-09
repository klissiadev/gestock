from fastapi import APIRouter, HTTPException
from admin_module.models.hardware_monitor import HardwareMonitor

router = APIRouter(tags=["Módulo de Adminstração"])

hardware_checker = HardwareMonitor()

@router.get("/hardware")
async def get_system_status():
    """
    Retorna o status em tempo real do servidor (consulo de CPU/GPU/RAM e DISCO)
    """
    try:
        data = hardware_checker.get_metrics()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter status: {str(e)}")