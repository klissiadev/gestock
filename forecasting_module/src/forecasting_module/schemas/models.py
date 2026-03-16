from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class FieldSaida(BaseModel):
    id: int
    produto_id: int
    quantidade: Decimal
    data_de_venda: date
    preco_de_venda: Decimal
    