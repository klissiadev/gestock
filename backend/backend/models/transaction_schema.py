from pydantic import BaseModel, field_serializer
from datetime import date, datetime
from typing import Optional

class TransactionSchema(BaseModel):
    unique_id: str
    produto_nome: str
    quantidade: int
    data_evento: date
    valor_unitario: Optional[float] = None 
    parceiro_origem: str
    local_destino: str
    tipo_movimento: str
    created_at: datetime

    @field_serializer('data_evento')
    def serialize_evento(self, data_evento: date):
        return data_evento.strftime('%d/%m/%Y')

    @field_serializer('created_at')
    def serialize_created(self, created_at: datetime):
        return created_at.strftime('%d/%m/%Y %H:%M')

    class Config:
        from_attributes = True