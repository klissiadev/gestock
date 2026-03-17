from fastapi import APIRouter, Depends, Query, Request
from forecasting_module.schemas.models import SugestaoCompraInsumo
from forecasting_module.db.database import Repository
import psycopg

router = APIRouter(prefix="/previsao", tags=["Previsão"])

async def get_db_connection(request: Request):
    """Busca uma conexão da ConnectionPool do backend"""
    async with request.app.state.db_pool.connection() as conn:
        yield conn

@router.get("/sugestoes-compra-insumos", response_model=list[SugestaoCompraInsumo])
async def obter_sugestoes_compra(
    connection: psycopg.AsyncConnection = Depends(get_db_connection),
    atualizar_view: bool = Query(False, description="Força a atualização da view materializada")
):
    """
    Calcula a necessidade de compra de matérias-primas baseada no déficit 
    dos Produtos Acabados e na explosão da ficha técnica usando psycopg3.
    """
    
    if atualizar_view:
        await connection.execute("REFRESH MATERIALIZED VIEW app_core.vw_product;")
        
    repo = Repository(conexao=connection)
    resultados = await repo.necessidade_compra() 
    
    return resultados
    
    