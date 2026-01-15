from llm_module.utils.postgres_client import PostgresClient
from langchain.tools import tool
import os
import unicodedata
from datetime import date

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
    
def _normalizar_variacoes(termo: str) -> list[str]:
    def strip_accents(s):
        return "".join(
            c for c in unicodedata.normalize("NFKD", s.lower())
            if not unicodedata.combining(c)
        )

    base = strip_accents(termo)
    variacoes = {base}

    if base.endswith("oes"):
        variacoes.add(base[:-3] + "ao")
    elif base.endswith("ais"):
        variacoes.add(base[:-3] + "al")
    elif base.endswith("eis"):
        variacoes.add(base[:-3] + "el")
    elif base.endswith("ois"):
        variacoes.add(base[:-3] + "ol")
    elif base.endswith("s") and len(base) > 3:
        variacoes.add(base[:-1])

    return sorted(variacoes)


@tool
def tool_buscar_produto(termo: str) -> dict:
    """
    Busca produtos no sistema a partir de um termo livre do usuário.
    A normalização e variações são tratadas internamente.
    Retorna o produto com os campos: nome_produto, descricao, estoque_atual, estoque_minimo, ativo, data_validade
    """
    
    where_ilike = " OR ".join(
        f"nome_produto ILIKE '%{v}%'"
        for v in _normalizar_variacoes(termo)
    )

    query = f"""
        SELECT
            nome_produto,
            descricao,
            estoque_atual,
            estoque_minimo,
            ativo,
            data_validade
        FROM app_core.v_produtos
        WHERE {where_ilike}
        ORDER BY nome_produto;
    """

    return _wrap_rows(database.fetch_all(query=query))


@tool
def tool_buscar_movimentacao(termo: str) -> dict:
    """
    Busca movimentações (entrada e saída) a partir de um termo livre do usuário.
    A normalização e variações são tratadas internamente.
    Retorna o produto com os campos: nome_produto, quantidade, data_movimentacao, entidade, tipo_movimentacao, adicionado_em
    """
    
    where_ilike = " OR ".join(
        f"nome_produto ILIKE '%{v}%'"
        for v in _normalizar_variacoes(termo)
    )

    query = f"""
        SELECT
            nome_produto,
            quantidade,
            data_movimentacao,
            entidade,
            tipo_movimentacao,
            adicionado_em
        FROM app_core.v_movimentacao
        WHERE {where_ilike}
        ORDER BY data_movimentacao DESC;
    """

    return _wrap_rows(database.fetch_all(query=query))


@tool
def tool_listar_produtos(apenas_ativos: bool = True) -> dict:
    """
    Lista produtos do sistema. Pode filtrar apenas os ativos.
    Retorna o produto com os campos: nome_produto, descricao, estoque_atual
    """

    filtro = "WHERE ativo = true" if apenas_ativos else ""

    query = f"""
        SELECT
            nome_produto,
            descricao,
            estoque_atual
        FROM app_core.v_produtos
        {filtro}
        ORDER BY nome_produto;
    """

    return _wrap_rows(database.fetch_all(query=query))


@tool
def tool_listar_movimentacoes(tipo: str = None) -> dict:
    """
    Lista movimentações do sistema. 
    É possivel filtrar por tipo: 
    'entrada': apenas movimentaçoes de entrada; 
    'saida': apenas movimentações de saída;
    None: Movimentações de ambos os tipos.
    Retorna o produto com os campos: nome_produto, quantidade, tipo_movimentacao, data_movimentacao
    """

    filtro = ""
    if tipo in ("entrada", "saida"):
        filtro = f"WHERE tipo_movimentacao = '{tipo}'"

    query = f"""
        SELECT
            nome_produto,
            quantidade,
            tipo_movimentacao,
            data_movimentacao
        FROM app_core.v_movimentacao
        {filtro}
        ORDER BY data_movimentacao DESC;
    """

    return _wrap_rows(database.fetch_all(query=query))


@tool
def tool_calcular_validade(data_validade: str) -> str:
    """
    Calcula o status de validade de um produto.
    """

    hoje = date.today()
    validade = date.fromisoformat(data_validade)
    dias = (validade - hoje).days

    if dias < 0:
        return f"Produto vencido há {-dias} dias."
    elif dias == 0:
        return "Produto vence hoje."
    elif dias <= 30:
        return f"Produto vence em {dias} dias."
    else:
        return f"Produto válido. Faltam {dias} dias para o vencimento."


@tool
def tool_consultar_item(termo: str, contexto: str) -> dict:
    """
        Consulta um item no sistema conforme o contexto solicitado.

        contexto pode ser:
        - "existencia"
        - "listar"
        - "movimentacao"
        - "validade"
    """
    if contexto == "existencia":
        return buscar_produto_base(termo)

    if contexto == "listar":
        return buscar_produto_detalhado(termo)

    if contexto == "movimentacao":
        return buscar_movimentacao_item(termo)

    if contexto == "validade":
        return buscar_validade_item(termo)

    return {
        "erro": "Contexto de consulta inválido."
    }


def testes():
    print("testando tool: Tool buscar produto com o termo 'placas'")
    print(tool_buscar_produto("PARAfuso"))
    
    print("testando tool: Tool buscar movimentação com o termo 'placas'")
    print(tool_buscar_movimentacao("placas"))
    
    print("testando tool: Tool listar produtos ativos")
    print(tool_listar_produtos(apenas_ativos=True))
    
    print("testando tool: Tool listar todas movimentações")
    print(tool_listar_movimentacoes(tipo=None))
    
    print("testando tool: Tool calcular validade para 2024-12-31")
    print(tool_calcular_validade("2024-12-31"))
    
    
    
if __name__ == "__main__":
    testes()