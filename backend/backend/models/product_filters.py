from pydantic import BaseModel
from typing import Optional

class product_filters(BaseModel):
    orderBy: str
    isAsc: bool
    search: Optional[str] = None

    # Filtro por: categoria, preco max e min
    categoria: Optional[str] = None
    isBaixoEstoque: bool = False
    isVencido: bool = False

    # preco_min: Optional[float] = None
    # preco_max: Optional[float] = None
    
