from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# =========================
# SCHEMAS PARA IMPORTAÇÃO
# =========================

PRODUTO_SCHEMA = {
    "table": "Produto",
    "columns": {
        "nome": {"type": "str", "required": True},
        "descricao": {"type": "str", "required": False},
        "categoria": {"type": "str", "required": True},
        "estoque_atual": {"type": "int", "required": True},
        "estoque_minimo": {"type": "int", "required": True},
        "data_cadastro": {"type": "date", "required": True, "format": "%Y-%m-%d"},
        "data_validade": {"type": "date", "required": False, "format": "%Y-%m-%d"},
        "valor_unitario": {"type": "float", "required": True},
    }
}

MOVIMENTACAO_SCHEMA = {
    "table": "Movimentacao",
    "columns": {
        "tipo_movimento": {"type": "str", "required": True},
        "data_movimento": {"type": "date", "required": True, "format": "%Y-%m-%d"},
        "quantidade": {"type": "int", "required": True},
        "observacao": {"type": "str", "required": False},
        "id_usuario": {"type": "int", "required": True},
        "cod_produto": {"type": "int", "required": True},
    }
}

IMPORT_SCHEMAS = {
    "Produto": PRODUTO_SCHEMA,
    "Movimentacao": MOVIMENTACAO_SCHEMA
}

# =========================
# CLASSES PYDANTIC
# =========================

# -------------------------
# PRODUTO
# -------------------------
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

# -------------------------
# MOVIMENTAÇÃO
# -------------------------
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

# -------------------------
# LOG DE IMPORTAÇÃO
# -------------------------
class LogImportacaoBase(BaseModel):
    nome_arquivo: str
    qntd_registros: int
    data_importacao: date  # ou datetime se preferir
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
