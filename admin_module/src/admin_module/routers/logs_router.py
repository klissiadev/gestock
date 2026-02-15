from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import date
from typing import Literal
from admin_module.models.logs_fetcher import LogFetcher
from admin_module.pydantic.logs_model import MinervaLogsRequest, ImportLogsRequest

router = APIRouter(tags=["Módulo de Administração"], prefix="/admin")
log_fetcher = LogFetcher()


@router.post("/logs/minerva")
def fetch_minerva_logs(request: MinervaLogsRequest):
    try:
        logs = log_fetcher.get_llm_log(
            user_name=request.user_name,
            period=request.period
        )
        if not logs:
            return {"logs": [], "message": "Nenhum registro encontrado para os filtros aplicados."}
        return {"total": len(logs), "logs": logs}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log do erro pode ser adicionado aqui usando o logger configurado
        raise HTTPException(status_code=500, detail="Erro interno no servidor: " + str(e))

@router.post("/logs/importacao")
def fetch_import_logs(request: ImportLogsRequest):
    """
    Endpoint para buscar logs de importação de arquivos.
    Suporta filtros por status, período, busca textual e ordenação.
    """
    try:
        logs = log_fetcher.get_import_log(
            direction=request.direction,
            order_by=request.order_by,
            search_term=request.search_term,
            status=request.status,
            periodo=request.periodo,
            apenas_erro=request.apenas_erro
        )
        
        return {
            "total": len(logs),
            "logs": logs
        }

    except Exception as e:
        # Logar o erro internamente é sempre bom
        print(f"Erro na rota /logs/importacao: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Falha ao recuperar logs de importação.")