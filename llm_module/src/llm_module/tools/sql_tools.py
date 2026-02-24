from llm_module.utils.postgres_client import PostgresClient
from langchain.tools import tool
from datetime import date
import unicodedata
from typing import Literal, Optional
from datetime import datetime
from langchain_core.tools import BaseTool

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
    Busca informações e detalhes cadastrais de um produto específico. 
    Use para saber se um item existe, ver sua descrição completa, 
    consultar a quantidade no estoque atual, o estoque mínimo ou a data de validade.
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
    Consulta o histórico de movimentações de UM produto específico. 
    Use quando o usuário quiser saber "o que aconteceu com a peça X", 
    "quem retirou o item Y" ou "quando compramos o produto Z".
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
    Lista o catálogo geral e amplo de produtos cadastrados no sistema. 
    Use quando o usuário pedir para "listar todos os produtos", "mostrar o catálogo" 
    ou "ver o que temos no sistema" de forma genérica, sem buscar um item específico.
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
    Lista o fluxo geral e recente de movimentações do estoque todo. 
    Use para ver as últimas entradas (compras) ou saídas (vendas) do sistema 
    como um todo, sem filtrar por produto ou data específica.
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
    Calcula apenas quantos dias faltam para uma data isolada vencer.
    Use estritamente como uma calculadora de tempo se precisar fazer 
    cálculo matemático de dias entre hoje e uma data específica.
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
    Lista produtos que estão próximos da data de vencimento ou que já estragaram. 
    Use quando o usuário perguntar: "o que vai vencer?", "produtos estragando", 
    ou "vencimentos até o dia X". (Data no formato YYYY-MM-DD).
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
    Identifica produtos em estado crítico ou em falta. 
    Use para responder perguntas como: "o que está faltando?", "o que está acabando?", 
    "o que precisamos comprar?", ou "quais itens atingiram o estoque mínimo?".
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
    Gera um relatório amplo de movimentações em um intervalo de datas (período). 
    Use para analisar períodos maiores que um único dia, como: "movimentações do mês passado", 
    "entradas da última semana", "resumo do trimestre". Exige datas (YYYY-MM-DD).
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
    Faz uma pesquisa ampla pelo texto da descrição dos produtos, não pelo nome principal. 
    Use quando o usuário procurar por uma característica, marca, categoria, cor 
    ou detalhe específico que não faz parte do nome do item.
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
def buscar_movimentacoes_por_data(data: str, tipo: str = None):
    """
    Consulta tudo o que aconteceu no estoque em UM ÚNICO dia específico. 
    Use para perguntas focadas no tempo: "o que movimentou hoje?", "vendas de ontem?", 
    "o que chegou no dia X?". (Sempre converta a data para YYYY-MM-DD).
    """
    
    # 1. Validação e Normalização da Data
    # Isso garante que a query não quebre se a LLM enviar "25/12/2023"
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

@tool
def buscar_movimentacoes_por_entidade(entidade: str, tipo: str = None, limite: int = 20):
    """
    Busca o histórico de ações de uma pessoa ou empresa (fornecedor, cliente, funcionário). 
    Use focado em QUEM fez a ação: "o que o João pegou?", "o que a empresa X entregou?", 
    "quem levou tal coisa?".
    """
    where_ilike = " OR ".join(
        f"entidade ILIKE '%{v}%'"
        for v in _normalizar_variacoes(entidade)
    )
    
    filtro_tipo = ""
    if tipo in ("entrada", "saida"):
        filtro_tipo = f" AND tipo_movimentacao = '{tipo}'"

    query = f"""
        SELECT
            nome_produto,
            quantidade,
            data_movimentacao,
            entidade,
            tipo_movimentacao,
            adicionado_em
        FROM app_core.v_movimentacao
        WHERE ({where_ilike}) {filtro_tipo}
        ORDER BY data_movimentacao DESC
        LIMIT {limite};
    """
    
    return _wrap_rows(database.fetch_all(query=query))

@tool
def top_produtos_movimentados(tipo: str = "saida", limite: int = 5):
    """
    Gera um ranking estatístico dos produtos mais movimentados. 
    Use para responder perguntas como: "quais itens saem mais?", "produtos mais consumidos", 
    "itens mais vendidos", "campeões de venda" ou "mais comprados".
    """
    # Validação simples
    tipo = tipo.lower() if tipo else "saida"
    if tipo not in ["entrada", "saida"]:
        tipo = "saida"

    query = f"""
        SELECT
            nome_produto,
            SUM(quantidade) as quantidade_total
        FROM app_core.v_movimentacao
        WHERE tipo_movimentacao = '{tipo}'
        GROUP BY nome_produto
        ORDER BY quantidade_total DESC
        LIMIT {limite};
    """
    
    return _wrap_rows(database.fetch_all(query=query))

@tool
def buscar_inconsistencias_estoque():
    """
    Realiza auditoria para encontrar falhas de registro no banco de dados. 
    Use para listar produtos desativados (inativos) que ainda constam com saldo 
    (estoque maior que zero), identificando erros no sistema.
    """
    query = """
        SELECT
            nome_produto,
            descricao,
            estoque_atual,
            ativo
        FROM app_core.v_produtos
        WHERE ativo = false AND estoque_atual > 0
        ORDER BY estoque_atual DESC;
    """
    
    return _wrap_rows(database.fetch_all(query=query))


MINERVA_SQL_TOOLS = [
    obj for nome, obj in globals().items() 
    if isinstance(obj, BaseTool)
]