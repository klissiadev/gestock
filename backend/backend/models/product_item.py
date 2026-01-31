from pydantic import BaseModel, field_serializer
from datetime import date
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    nome: str
    tipo: str
    descricao: Optional[str]
    estoque_atual: int
    estoque_minimo: int
    baixo_estoque: bool
    vencido: bool
    data_validade: date
    ativo: bool

    @field_serializer('data_validade')
    def serialize_date(self, data_validade: date):
        return data_validade.strftime('%d/%m/%Y')

    class Config:
        from_attributes = True 