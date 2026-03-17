from fastapi import APIRouter, Depends, Query, Request
from forecasting_module.schemas.models import SugestaoCompraInsumo, PontoGrafico, ProdutoDropdown
from forecasting_module.db.database import Repository
import psycopg

router = APIRouter(prefix="/previsao", tags=["Previsão"])

async def get_db_connection(request: Request):
    """Busca uma conexão da ConnectionPool do backend"""
    async with request.app.state.db_pool.connection() as conn:
        yield conn


@router.get("/produtos-com-historico", response_model=list[ProdutoDropdown])
async def obter_produtos_para_grafico(
    connection: psycopg.AsyncConnection = Depends(get_db_connection)
):
    """
    Retorna apenas os produtos acabados que possuem movimentação de saída,
    ideal para popular selects/dropdowns no frontend.
    """
    repo = Repository(conexao=connection)
    produtos = await repo.listar_produtos_com_vendas()
    return produtos


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

@router.get("/{produto_id}", response_model=list[PontoGrafico])
async def obter_previsao_demanda(
    produto_id: int,
    connection: psycopg.AsyncConnection = Depends(get_db_connection)
):
    """
    Previsão de Demanda com base na média móvel dos ultimos 3 meses.
    
    Média movel Exponencial dá maior peso aos dados mais recentes, assim ela é mais sensível às mudanças recentes no comportamento dos dados. 
    Isso a torna mais eficaz para identificar tendências a curto prazo.
    """
    repo = Repository(conexao=connection)
    
    # Pega os dados reais do banco
    historico_db = await repo.buscar_historico_saidas(produto_id)
    
    if not historico_db:
        return [] # Sem histórico, sem previsão
    
    # Inicio do calculo
    dados_grafico = []
    N = 3 # últimos 3 meses
    alpha = 2 / (N + 1) # Fator de suavização 
    mme_anterior = None # Nao ha mme anterior
    
    # Calcula a MME para o histórico
    for i in range(len(historico_db)):
        demanda_atual = float(historico_db[i]["demanda_real"])
        mes = historico_db[i]["mes"]
        
        if mme_anterior is None:
            # O ponto de partida da MME = demanda do 1º mês
            mme_atual = demanda_atual
        else:
            # Forma aplicando peso maior ao dado recente
            mme_atual = (demanda_atual * alpha) + (mme_anterior * (1 - alpha))
            
        dados_grafico.append({
            "mes": mes,
            "demanda_real": demanda_atual,
            "previsao": round(mme_atual, 2)
        })
        
        # Guarda o valor calculado para usar na próxima iteração
        mme_anterior = mme_atual
    
    if mme_anterior is not None:
        dados_grafico.append({
            "mes": "Próximo Mês (Previsão)",
            "demanda_real": None, # Ainda não aconteceu
            "previsao": round(mme_anterior, 2)
        })

    return dados_grafico



    