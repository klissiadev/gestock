from fastapi import APIRouter, Depends
from backend.services.views_service import view_service
from backend.database.base import get_db

router = APIRouter(prefix="/views", tags=["visualizar"])

@router.post(path="/product")
async def testando_tabela(db = Depends(get_db)):
    view = view_service(db)
    return view.see_product_table()
