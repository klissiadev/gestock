from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class FieldSaida(BaseModel):
    id: int
    produto_id: int
    quantidade: Decimal
    data_de_venda: date
    preco_de_venda: Decimal
    
class SugestaoCompraInsumo(BaseModel):
    materia_prima_id: int
    nome_materia_prima: str
    quantidade_sugerida_compra: float
    
class PontoGrafico(BaseModel):
    mes: str
    demanda_real: float | None 
    previsao: float | None
    
class ProdutoDropdown(BaseModel):
    id: int
    nome: str
    
