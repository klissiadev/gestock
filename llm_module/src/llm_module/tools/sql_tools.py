from llm_module.utils.postgres_client import PostgresClient
from langchain.tools import tool
from datetime import date, datetime
import unicodedata
from typing import Optional

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
    "Cria uma lista de variações de um termo de busca"
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

def _normalizar_data(data_str: str) -> str:
    """Tenta adivinhar e padronizar o formato da data para YYYY-MM-DD."""
    if not data_str or data_str.lower() in ['hoje', 'today']:
        return date.today().strftime("%Y-%m-%d")
        
    ano_atual = datetime.now().year
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m", "%d-%m"]
    
    for formato in formatos:
        try:
            dt = datetime.strptime(data_str.strip(), formato)
            if dt.year == 1900: # Se o usuário passou só dia/mês
                dt = dt.replace(year=ano_atual)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return data_str

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
def tool_buscar_movimentacao(termo: str, tipo: Optional[str] = None) -> dict:
    """Busca movimentações. Retorna: produto_nome, quantidade, data_evento, valor_unitario, parceiro_origem, local_destino, tipo_movimento"""
    where_clauses = []
    if termo:
        # Note que a coluna agora é produto_nome
        where_ilike = " OR ".join(f"produto_nome ILIKE '%{v}%'" for v in _normalizar_variacoes(termo))
        where_clauses.append(f"({where_ilike})")
    
    if tipo in ("entrada", "saida"):
        where_clauses.append(f"tipo_movimento = '{tipo}'")
    
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = f"""
        SELECT produto_nome, quantidade, data_evento, valor_unitario, parceiro_origem, local_destino, tipo_movimento
        FROM app_core.mv_movimentacao {where_sql} ORDER BY data_evento DESC;
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
def tool_listar_movimentacoes(tipo: Optional[str] = None) -> dict:
    """Lista movimentações do sistema por tipo ('entrada' ou 'saida')."""
    filtro = f"WHERE tipo_movimento = '{tipo}'" if tipo in ("entrada", "saida") else ""
    query = f"""
        SELECT produto_nome, quantidade, tipo_movimento, data_evento, parceiro_origem, local_destino
        FROM app_core.mv_movimentacao {filtro} ORDER BY data_evento DESC;
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
def buscar_produtos_a_vencer(data: Optional[str] = None, termo: str = ""):
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
def buscar_movimentacoes_por_periodo(data_inicio: str, data_fim: str, tipo: Optional[str] = None):
    """Busca movimentações num intervalo. Retorna colunas da mv_movimentacao."""
    dt_ini = _normalizar_data(data_inicio)
    dt_fim = _normalizar_data(data_fim)
    filtro_tipo = f"AND tipo_movimento = '{tipo.upper()}'" if tipo in ("entrada", "saida") else ""

    # ::date assegura que o BETWEEN funciona com a data pura, ignorando as horas do timestamp
    query = f"""
        SELECT produto_nome, quantidade, data_evento, valor_unitario, parceiro_origem, local_destino, tipo_movimento
        FROM app_core.mv_movimentacao
        WHERE data_evento::date BETWEEN '{dt_ini}' AND '{dt_fim}' {filtro_tipo}
        ORDER BY data_evento DESC;
    """
    return _wrap_rows(database.fetch_all(query=query))

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


@tool
def buscar_movimentacoes_por_data(data: str, tipo: Optional[str] = None):
    """Consulta movimentações para uma data específica (converte 'hoje' ou 'DD/MM' auto)."""
    data_formatada = _normalizar_data(data)
    
    try: # Checagem rápida para ver se a função '_normalizar_data' conseguiu criar um YYYY-MM-DD
        datetime.strptime(data_formatada, "%Y-%m-%d")
    except ValueError:
        return f"Erro: O formato da data '{data}' é inválido ou não compreendido."

    filtro_tipo = f"AND tipo_movimento = '{tipo.upper()}'" if tipo in ("entrada", "saida") else ""

    print(f"DEBUG: data_formatada: {data_formatada} e o tipo: {tipo}")

    query = f"""
        SELECT produto_nome, quantidade, data_evento, valor_unitario, parceiro_origem, local_destino, tipo_movimento
        FROM app_core.mv_movimentacao
        WHERE data_evento::date = '{data_formatada}' {filtro_tipo}
        ORDER BY created_at DESC;
    """

    print(f"QUERY: {query}")

    rows = database.fetch_all(query=query)
    print(f"Resposta: {rows}")
    if not rows:
        return f"Não encontrei nenhuma movimentação no dia {data_formatada}."
    return _wrap_rows(rows)