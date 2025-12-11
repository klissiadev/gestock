from pydantic import BaseModel
from datetime import date
from typing import Optional
IMPORT_SCHEMAS = {
    "products": {
        "required_columns": ["id", "name", "sku", "unit", "price"]
    },
    "stock": {
        "required_columns": ["product_id", "quantity", "location"]
    },
    "movimentacoes": {
        "required_columns": ["product_id", "tipo", "quantidade", "data"]
    }
}
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    categoria: str
    estoque_atual: int
    estoque_minimo: int
    data_cadastro: date
    data_validade: Optional[date] = None
    valor_unitario: float


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    estoque_atual: Optional[int] = None
    estoque_minimo: Optional[int] = None
    data_cadastro: Optional[date] = None
    data_validade: Optional[date] = None
    valor_unitario: Optional[float] = None


class ProdutoOut(ProdutoBase):
    cod_produto: int
    
class MovimentacaoBase(BaseModel):
    tipo_movimento: str
    data_movimento: date
    quantidade: int
    observacao: Optional[str] = None
    id_usuario: int
    cod_produto: int


class MovimentacaoCreate(MovimentacaoBase):
    pass


class MovimentacaoOut(MovimentacaoBase):
    id_movimentacao: int
    
    