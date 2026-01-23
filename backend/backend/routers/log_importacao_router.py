#backend\backend\routers\log_importacao_router.py
from fastapi import APIRouter, Depends, HTTPException
from backend.database.base import get_connection
from backend.services.log_importacao_service import LogImportacaoService
from typing import List

router = APIRouter(prefix="/logs-importacao", tags=["Logs de Importação"])

def get_service(conn = Depends(get_connection)):
    return LogImportacaoService(conn)

@router.post("/")
def criar_log(log_data: dict, service: LogImportacaoService = Depends(get_service)):
    return service.criar_log(log_data)

@router.get("/")
def listar_logs(service: LogImportacaoService = Depends(get_service)):
    return service.listar_logs()

@router.get("/{log_id}")
def buscar_log(log_id: int, service: LogImportacaoService = Depends(get_service)):
    return service.buscar_por_id(log_id)

@router.put("/{log_id}")
def atualizar_log(log_id: int, dados_atualizacao: dict, service: LogImportacaoService = Depends(get_service)):
    return service.atualizar_log(log_id, dados_atualizacao)

@router.delete("/{log_id}")
def deletar_log(log_id: int, service: LogImportacaoService = Depends(get_service)):
    return service.deletar_log(log_id)