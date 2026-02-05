from fastapi import APIRouter, HTTPException
from admin_module.models.system_health import SystemHealth

router = APIRouter(tags=["Monitoring"])

health_checker = SystemHealth()

@router.get("/health")
async def get_system_status():
    """
    Retorna o status em tempo real do Banco, Ollama e SMTP.
    """
    try:
        data = health_checker.get_all_statuses()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter status: {str(e)}")