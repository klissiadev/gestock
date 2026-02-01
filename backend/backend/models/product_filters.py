from pydantic import BaseModel
from typing import Optional

class product_filters(BaseModel):
    orderBy: str
    isAsc: bool
    searchTerm: Optional[str] = None
    categoria: Optional[str] = None
    isBaixoEstoque: bool = False
    isVencido: bool = False

    
