from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# =========================
# IMPORTAÇÃO (CONFIG)
# =========================

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

# =========================
# PRODUTO
# =========================

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

# =========================
# MOVIMENTAÇÃO
# =========================

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

# =========================
# LOG DE IMPORTAÇÃO
# =========================

class LogImportacaoBase(BaseModel):
    nome_arquivo: str
    qntd_registros: int
    data_importacao: date  # pode ser datetime se preferir
    status: str
    msg_erro: Optional[str] = None
    id_usuario: int


class LogImportacaoCreate(LogImportacaoBase):
    pass


class LogImportacaoUpdate(BaseModel):
    nome_arquivo: Optional[str] = None
    qntd_registros: Optional[int] = None
    data_importacao: Optional[date] = None
    status: Optional[str] = None
    msg_erro: Optional[str] = None
    id_usuario: Optional[int] = None


class LogImportacaoOut(LogImportacaoBase):
    id_log_importacao: int
