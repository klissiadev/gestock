from pydantic import BaseModel
from typing import Optional

class product_filters(BaseModel):
    orderBy: str
    isAsc: bool
    search: Optional[str] = None

    # Filtro por: categoria, preco max e min
    categoria: Optional[str] = None

    # preco_min: Optional[float] = None
    # preco_max: Optional[float] = None
    
    # Filtros logicos
    # apenas_baixo_estoque: bool = False
    # apenas_vencidos: bool = False