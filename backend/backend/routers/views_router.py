from fastapi import APIRouter, Depends
from typing import List
from backend.services.views_service import view_service
from backend.database.base import get_db
from backend.models.product_filters import product_filters
from backend.models.transaction_filters import transaction_filters
from backend.models.product_item import ProductSchema
from backend.models.transaction_schema import TransactionSchema

router = APIRouter(prefix="/views", tags=["visualizar"])

@router.post("/product", response_model=List[ProductSchema])
async def exibir_tabela_produto(filter: product_filters, db=Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"
    
    view = view_service(db)
    return view.see_product_table(
        direcao=direcao,
        order_by=filter.orderBy,
        search_term=filter.searchTerm,
        tipo=filter.categoria,
        apenas_baixo_estoque=filter.isBaixoEstoque,
        apenas_vencidos=filter.isVencido
    )



@router.post(path="/moviment", response_model=List[TransactionSchema])
async def exibir_tabela_movimentacao(filter: transaction_filters, db = Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"
    
    view = view_service(db)

    return view.see_transaction_table(
        direcao=direcao, 
        order_by=filter.orderBy, 
        search_term=filter.search
    )
