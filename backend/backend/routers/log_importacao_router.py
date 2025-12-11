from fastapi import APIRouter, HTTPException
from backend.models.log_importacao import LogImportacaoCreate, LogImportacao
from backend.services.log_importacao_service import criar_log_importacao

router = APIRouter(
    prefix="/log-importacao",
    tags=["Log de Importação"]
)


@router.post("/", response_model=LogImportacao)
def criar_log(log: LogImportacaoCreate):
    try:
        novo_log = criar_log_importacao(log)
        return novo_log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
