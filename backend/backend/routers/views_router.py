from fastapi import APIRouter, Depends
from backend.services.views_service import view_service
from backend.database.base import get_db
from backend.models.product_filters import product_filters

router = APIRouter(prefix="/views", tags=["visualizar"])



@router.post(path="/product")
async def testando_tabela(filter: product_filters, db = Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"
    order_by = filter.orderBy
    search_term = filter.search
    category = filter.categoria
    is_baixo_estoque = filter.isBaixoEstoque
    is_vencidos = filter.isVencido

    view = view_service(db)
    return view.see_product_table(direcao, order_by, search_term, category, is_baixo_estoque, is_vencidos)

@router.post(path="/moviment")
async def testando_tabela_moviment(db = Depends(get_db)):
    view = view_service(db)
    return view.see_movimentacao_table()

