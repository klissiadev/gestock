"""
Docstring for llm_module.tools.sql_tools

Aqui você encontra todas as tools relacionadas a SQL que a LLM pode utilizar
para cumprir o seu trabalho.

Por enquanto ela pode:
- listar_produtos(limite)
- buscar_produto_por_nome(nome)
- produtos_vencendo(dias)
- produtos_vencimento_proximo()
- contagem_produtos()
"""

from llm_module.utils.postgres_client import PostgresClient
from langchain.tools import tool
import os

# Instância única do cliente de banco (ok para uso atual)
database = PostgresClient()

def _wrap_rows(rows: list[dict]) -> dict:
    """
    Padroniza o retorno para consumo da LLM.
    """
    return {
        "total": len(rows),
        "items": rows,
        "empty": len(rows) == 0
    }


@tool
def tool_listar_produtos(limite: int | None = None) -> dict:
    """ Lista os produtos no banco de dados. - limite: opcional (máx definido por MAX_QUERY_LIMIT, padrão 500) """
    max_limit = int(os.getenv("MAX_QUERY_LIMIT", "500"))

    if limite is None:
        limite = max_limit
    else:
        limite = min(limite, max_limit)

    query = """
        SELECT nome, descricao, estoque_minimo, data_validade
        FROM app_core.v_produtos
        ORDER BY nome
        LIMIT %s
    """

    rows = database.fetch_all(query, (limite,))
    return _wrap_rows(rows)


@tool
def tool_produtos_vencendo(dias: int) -> dict:
    """ Retorna produtos que vencem dentro de um número de dias informado. """
    query = """
        SELECT nome, descricao, estoque_minimo, data_validade
        FROM app_core.v_produtos
        WHERE data_validade IS NOT NULL
          AND data_validade <= CURRENT_DATE + (%s * INTERVAL '1 day')
        ORDER BY data_validade
    """

    rows = database.fetch_all(query, (dias,))
    return _wrap_rows(rows)


@tool
def tool_produtos_vencimento_proximo() -> dict:
    """ Retorna produtos com data de validade nos próximos 30 dias. """
    query = """
        SELECT *
        FROM app_core.v_produtos_vencimento_prox
        ORDER BY data_validade ASC
    """

    rows = database.fetch_all(query)
    return _wrap_rows(rows)

@tool
def tool_contagem_produtos() -> dict:
    """ Retorna a quantidade total de produtos cadastrados. """
    query = "SELECT total FROM app_core.v_contagem_produtos"
    rows = database.fetch_all(query)

    total = rows[0]["total"] if rows else 0

    return {
        "total": total,
        "items": [],
        "empty": total == 0
    }
