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
class Produto(BaseModel):
    nome: str
    descricao: Optional[str] = None
    estoque_minimo: int
    data_validade: Optional[date] = None
    ativo: bool = True

# -------------------------
# MOVIMENTAÇÃO de entrada
# -------------------------
class MovimentacaoEntrada(BaseModel):
    produto_id: int
    quantidade: int
    data_de_compra: date
    preco_de_compra: float
    fornecedor: str

# -------------------------
# MOVIMENTAÇÃO de saida
# -------------------------
class MovimentacaoSaida(BaseModel):
    produto_id: int
    quantidade: int
    data_de_venda: date
    preco_de_venda: float
    cliente: str

# -------------------------
# REQUEST DA LLM
# -------------------------
class LLMRequest(BaseModel):
    question: str
