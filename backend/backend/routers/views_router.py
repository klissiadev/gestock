from fastapi import APIRouter, Depends
from typing import List
from backend.services.views_service import view_service
from backend.database.base import get_db
from backend.models.product_filters import product_filters
from backend.models.moviment_filters import moviment_filters
from backend.models.product_item import ProductSchema

router = APIRouter(prefix="/views", tags=["visualizar"])

@router.post("/product", response_model=List[ProductSchema])
async def exibir_tabela_produto(filter: product_filters, db = Depends(get_db)):
        direcao = "ASC" if filter.isAsc else "DESC"

        COLUNAS_ORDENAVEIS = {
            "id", "nome", "tipo", "descricao", "estoque_minimo", "data_validade", "estoque_atual"
        }

        order_by = filter.orderBy if filter.orderBy in COLUNAS_ORDENAVEIS else "nome"
        search_term = filter.searchTerm
        category = filter.categoria.strip() if filter.categoria else None

        view = view_service(db)
        return view.see_product_table(
            direcao,
            order_by,
            search_term,
            category,
            filter.isBaixoEstoque,
            filter.isVencido
        )



@router.post(path="/moviment")
async def exibir_tabela_movimentacao(filter: moviment_filters, db = Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"

    COLUNAS_ORDENAVEIS = {
        "id",
        "produto_id",
        "ordem_de_producao",
        "tipo",
        "quantidade",
        "origem",
        "destino",
        "data"
    }

    order_by = filter.orderBy if filter.orderBy in COLUNAS_ORDENAVEIS else "id"
    search_term = filter.search
    
    view = view_service(db)
    return view.see_movimentacao_table(direcao, order_by, search_term)

