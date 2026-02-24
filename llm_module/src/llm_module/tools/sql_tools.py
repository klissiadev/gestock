from llm_module.utils.postgres_client import PostgresClient
from langchain.tools import tool
from datetime import date
import unicodedata

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
def tool_buscar_movimentacao(termo: str, tipo: str = None) -> dict:
    """
    Busca movimentações (entrada e saída) a partir de um termo livre do usuário.
    A normalização e variações são tratadas internamente.
    Valor Padrao de tipo: None -> busca tanto entradas quanto saídas
    Retorna o produto com os campos: nome_produto, quantidade, data_movimentacao, entidade, tipo_movimentacao, adicionado_em
    """
    
    # Condição para o termo
    where_clauses = []
    if termo:
        where_ilike = " OR ".join(
            f"nome_produto ILIKE '%{v}%'"
            for v in _normalizar_variacoes(termo)
        )
        where_clauses.append(f"({where_ilike})")
    
    # Condição para o tipo de movimentação
    if tipo in ("entrada", "saida"):
        where_clauses.append(f"tipo_movimentacao = '{tipo}'")
    
    # Junta as condições com AND, ou deixa vazio
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    query = f"""
        SELECT
            nome_produto,
            quantidade,
            data_movimentacao,
            entidade,
            tipo_movimentacao,
            adicionado_em
        FROM app_core.v_movimentacao
        {where_sql}
        ORDER BY data_movimentacao DESC;
    """

    rows = database.fetch_all(query=query)
    return _wrap_rows(rows)



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
def buscar_produtos_a_vencer(data: str = None, termo: str = ""):
    """
    Busca produtos no sistema que tenham uma data de validade menor do que a variável 'data' 
    e permite uso de termos de pesquisa, sendo isso opcional.
    'data' deve estar no padrão YYYY-MM-DD; valor padrão: data atual.
    Retorna os campos: nome_produto, descricao, estoque_atual, estoque_minimo, ativo, data_validade
    """
    # Se data não for informada, usa a data de hoje
    if data is None:
        data = date.today().isoformat()

    # Monta cláusula de termos, se fornecido
    where_ilike = ""
    if termo.strip():
        termos = " OR ".join(f"nome_produto ILIKE '%{v}%'" for v in _normalizar_variacoes(termo))
        where_ilike = f" AND ({termos})"

    query = f"""
    SELECT
        nome_produto,
        descricao,
        estoque_atual,
        estoque_minimo,
        ativo,
        data_validade
    FROM app_core.v_produtos
    WHERE data_validade < '{data}' {where_ilike}
    ORDER BY data_validade, nome_produto;
    """
    
    rows = database.fetch_all(query=query)
    return _wrap_rows(rows)

@tool
def buscar_produtos_abaixo_estoque(termo: str = ""):
    """
    Busca produtos no sistema que estejam abaixo do estoque
    e permite uso de termos de pesquisa, sendo isso opcional.
    Retorna os campos: nome_produto, descricao, estoque_atual, estoque_minimo, ativo, data_validade
    """
    where_term = ""
    if termo:
        termos = " OR ".join(f"nome_produto ILIKE '%{v}%'" for v in _normalizar_variacoes(termo))
        where_term = f" AND ({termos})"

    query = f"""
    SELECT
        nome_produto,
        descricao,
        estoque_atual,
        estoque_minimo,
        ativo,
        data_validade
    FROM app_core.v_produtos
    WHERE estoque_atual <= estoque_minimo {where_term}
    ORDER BY nome_produto;
    """
    
    rows = database.fetch_all(query=query)
    return _wrap_rows(rows)

@tool
def buscar_movimentacoes_por_periodo(data_inicio: str, data_fim: str, tipo: str = None):
    """
    Busca movimentações no sistema que tenham uma data de movimentação entre 'data_inicio' e 'data_fim'
    e permite filtro por tipo de movimentação (entrada ou saída).
    Retorna os campos: nome_produto, quantidade, data_movimentacao, entidade, tipo_movimentacao, adicionado_em
    """
    filtro_tipo = ""
    if tipo in ("entrada", "saida"):
        filtro_tipo = f"AND tipo_movimentacao = '{tipo}'"

    query = f"""
    SELECT
        nome_produto,
        quantidade,
        data_movimentacao,
        entidade,
        tipo_movimentacao,
        adicionado_em
    FROM app_core.v_movimentacao
    WHERE data_movimentacao BETWEEN '{data_inicio}' AND '{data_fim}' {filtro_tipo}
    ORDER BY data_movimentacao DESC;
    """
    
    rows = database.fetch_all(query=query)
    return _wrap_rows(rows)

@tool
def buscar_produtos_por_descricao(termo: str):
    """
    Busca produtos no sistema que tenham o termo fornecido na descrição.
    Retorna os campos: nome_produto, descricao, estoque_atual, estoque_minimo, ativo, data_validade
    """
    where_ilike = " OR ".join(
        f"descricao ILIKE '%{v}%'"
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


from typing import Literal, Optional
from datetime import datetime

@tool
def buscar_movimentacoes_por_data(data: str, tipo: str = None):
    """
    Consulta o histórico de movimentações (entradas/saídas) para uma data específica. Converta termos como 'hoje', 'ontem' ou 'dia 10 de maio' para o formato 'YYYY-MM-DD'.
    - Parametro data: string no formato 'YYYY-MM-DD'. Faça adaptações caso o usuário use termos como 'hoje', 'ontem' ou 'dia 10 de maio' ou outros formatos comuns. Se a data for inválida, avise o usuário.
    - O parâmetro 'tipo' só aceita 'entrada' ou 'saida'. Se o usuário não especificar, deixe None.
    """
    
    try:
        data_formatada = datetime.strptime(data.replace("/", "-"), "%Y-%m-%d").date()
    except ValueError:
        return f"Erro: O formato da data '{data}' é inválido. Use 'YYYY-MM-DD'."

    filtro_tipo = ""
    if tipo:
        tipo = tipo.lower().strip()
        if tipo in ["entrada", "saida"]:
            filtro_tipo = f"AND tipo_movimentacao = '{tipo}'"
        else:
            pass 
        
    print(f"Data formatada: {data_formatada}, Filtro tipo: '{filtro_tipo}'")  # Debug

    # 3. Montagem da Query
    query = f"""
    SELECT
        nome_produto,
        quantidade,
        data_movimentacao,
        entidade,
        tipo_movimentacao,
        adicionado_em
    FROM app_core.v_movimentacao
    WHERE data_movimentacao = '{data_formatada}' {filtro_tipo}
    ORDER BY adicionado_em DESC;
    """
    
    rows = database.fetch_all(query=query)
    
    if not rows:
        return f"Não encontrei nenhuma movimentação no dia {data_formatada}."
        
    return _wrap_rows(rows)

    
    
    
