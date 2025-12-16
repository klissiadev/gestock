from pydantic import BaseModel
from typing import Optional

class moviment_filters(BaseModel):
    orderBy: str
    isAsc: bool
    search: Optional[str] = None

    # Filtro por: tipo movimentacao e data
    tipoMovimentacao: Optional[str] = None  # 'entrada' ou 'saida'
    dataInicio: Optional[str] = None        # Formato 'YYYY-MM-DD'
    dataFim: Optional[str] = None           # Formato 'YYYY-MM-DD'