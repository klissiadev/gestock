from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# =========================
# SCHEMAS PARA IMPORTAÇÃO
# =========================

PRODUTO_SCHEMA = {
    "table": "app_core.produtos",
    "columns": {
        "nome": {"type": "str", "required": True},
        "descricao": {"type": "str", "required": False},
        "estoque_minimo": {"type": "int", "required": True},
        "data_validade": {"type": "date", "required": False, "format": "%Y-%m-%d"},
        "ativo": {"type": "bool", "required": False},
    }
}

MOVIMENTACAO_SAIDA_SCHEMA = {
    "table": "app_core.movimentacoes_saida",
    "columns": {
        "produto_id": {"type": "int", "required": True},
        "quantidade": {"type": "int", "required": True},
        "data_de_venda": {"type": "date", "required": True, "format": "%Y-%m-%d"},
        "preco_de_venda": {"type": "float", "required": True},
        "cliente": {"type": "str", "required": True},
    }
}

MOVIMENTACAO_ENTRADA_SCHEMA = {
    "table": "app_core.movimentacoes_entrada",
    "columns": {
        "produto_id": {"type": "int", "required": True},
        "quantidade": {"type": "int", "required": True},
        "data_de_compra": {"type": "date", "required": True, "format": "%Y-%m-%d"},
        "preco_de_compra": {"type": "float", "required": True},
        "fornecedor": {"type": "str", "required": True},
    }
}

IMPORT_SCHEMAS = {
    "produtos": PRODUTO_SCHEMA,
    "movimentacoes_entrada": MOVIMENTACAO_ENTRADA_SCHEMA,
    "movimentacoes_saida": MOVIMENTACAO_SAIDA_SCHEMA,
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
    estoque_minimo: int
    data_validade: Optional[date] = None
    ativo: bool = True

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    estoque_minimo: Optional[int] = None
    data_validade: Optional[date] = None
    ativo: Optional[bool] = None

class ProdutoOut(ProdutoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

# -------------------------
# MOVIMENTAÇÃO de entrada
# -------------------------
class MovimentacaoEntradaBase(BaseModel):
    produto_id: int
    quantidade: int
    data_de_compra: date
    preco_de_compra: float
    fornecedor: str

class MovimentacaoEntradaCreate(MovimentacaoEntradaBase):
    pass

class MovimentacaoEntradaOut(MovimentacaoEntradaBase):
    id: int
    created_at: datetime

# -------------------------
# MOVIMENTAÇÃO de saida
# -------------------------
class MovimentacaoSaidaBase(BaseModel):
    produto_id: int
    quantidade: int
    data_de_venda: date
    preco_de_venda: float
    cliente: str

class MovimentacaoSaidaCreate(MovimentacaoSaidaBase):
    pass

class MovimentacaoSaidaOut(MovimentacaoSaidaBase):
    id: int
    created_at: datetime

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
