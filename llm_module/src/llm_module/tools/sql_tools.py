from llm_module.utils.postgres_client import PostgresClient
from langchain.tools import tool
from datetime import date
import unicodedata

# Instância única do cliente de banco (ok para uso atual)
database = PostgresClient()

def _wrap_rows(rows: list[dict], limit: int = 20) -> dict:
    """Padroniza o retorno e avisa a LLM se os resultados foram truncados."""
    total_retornado = len(rows)
    return {
        "total_encontrado_na_busca": total_retornado,
        "items": rows,
        "aviso": f"Mostrando apenas os primeiros {limit} resultados para economizar memória. Peça para o usuário ser mais específico se o que ele procura não estiver aqui." if total_retornado >= limit else "Todos os resultados mostrados.",
        "empty": total_retornado == 0
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
def consultar_produtos(termo_busca: Optional[str] = None, buscar_na_descricao: bool = False, apenas_ativos: bool = True) -> dict:
    """
    SUPER FERRAMENTA DE PRODUTOS. Use SEMPRE que precisar buscar, listar ou saber informações de produtos no estoque.
    - Se o usuário quiser ver todos os produtos, não passe o 'termo_busca'.
    - Se o usuário procurar por um nome específico, passe em 'termo_busca'.
    - Se a busca pelo nome falhar, tente novamente passando 'buscar_na_descricao=True'.
    """
    where_clauses = []
    
    if apenas_ativos:
        where_clauses.append("ativo = true")
        
    if termo_busca:
        coluna = "descricao" if buscar_na_descricao else "nome_produto"
        where_ilike = " OR ".join(f"{coluna} ILIKE '%{v}%'" for v in _normalizar_variacoes(termo_busca))
        where_clauses.append(f"({where_ilike})")
        
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    # LIMIT 20 SALVA SUA JANELA DE CONTEXTO!
    query = f"""
        SELECT nome_produto, descricao, estoque_atual, estoque_minimo, ativo, data_validade
        FROM app_core.v_produtos
        {where_sql}
        ORDER BY nome_produto
        LIMIT 20; 
    """
    return _wrap_rows(database.fetch_all(query=query), limit=20)


@tool
def consultar_movimentacoes(
    produto: Optional[str] = None, 
    tipo: Optional[str] = None, 
    data_inicio: Optional[str] = None, 
    data_fim: Optional[str] = None
) -> dict:
    """
    SUPER FERRAMENTA DE MOVIMENTAÇÕES. Use para relatórios, histórico de entradas/saídas ou buscar dados de datas específicas.
    - 'tipo' DEVE ser apenas 'entrada', 'saida' ou null.
    - 'data_inicio' e 'data_fim' devem ser no formato YYYY-MM-DD.
    - Se o usuário pedir 'hoje', passe a data atual em ambos.
    """
    where_clauses = []
    
    if produto:
        where_ilike = " OR ".join(f"produto_nome ILIKE '%{v}%'" for v in _normalizar_variacoes(produto))
        where_clauses.append(f"({where_ilike})")
        
    if tipo in ("entrada", "saida"):
        where_clauses.append(f"tipo_movimento = '{tipo.upper()}'") # Assumindo que no banco fica uppercase
        
    if data_inicio:
        dt_ini = _normalizar_data(data_inicio)
        if data_fim:
            dt_fim = _normalizar_data(data_fim)
            where_clauses.append(f"data_evento::date BETWEEN '{dt_ini}' AND '{dt_fim}'")
        else:
            where_clauses.append(f"data_evento::date = '{dt_ini}'")

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
        SELECT produto_nome, quantidade, data_evento, valor_unitario, parceiro_origem, local_destino, tipo_movimento
        FROM app_core.mv_movimentacao 
        {where_sql} 
        ORDER BY data_evento DESC
        LIMIT 20;
    """
    return _wrap_rows(database.fetch_all(query=query), limit=20)


@tool
def relatorio_alertas_estoque(tipo_alerta: str = "ambos", data_referencia: Optional[str] = None) -> dict:
    """
    Use para descobrir problemas no estoque: produtos vencendo ou abaixo do mínimo.
    - 'tipo_alerta': use 'vencimento' (para produtos a vencer), 'estoque_baixo' (para repor estoque), ou 'ambos'.
    """
    where_clauses = []
    
    if tipo_alerta in ("estoque_baixo", "ambos"):
        where_clauses.append("(estoque_atual <= estoque_minimo)")
        
    if tipo_alerta in ("vencimento", "ambos"):
        data = data_referencia if data_referencia else date.today().isoformat()
        where_clauses.append(f"(data_validade < '{data}')")

    # Junta com OR se for ambos, ou AND se for outra coisa (aqui uma lógica simples usando OR atende bem um painel de alertas)
    where_sql = "WHERE " + " OR ".join(where_clauses) if where_clauses else ""

    query = f"""
        SELECT nome_produto, descricao, estoque_atual, estoque_minimo, data_validade
        FROM app_core.v_produtos
        {where_sql}
        ORDER BY data_validade ASC, estoque_atual ASC
        LIMIT 20;
    """
    return _wrap_rows(database.fetch_all(query=query), limit=20)

@tool
def ferramenta_sql_livre(query_sql: str) -> str | dict:
    """
    ÚLTIMO RECURSO: Use esta ferramenta APENAS se as outras ferramentas não puderem responder à pergunta.
    Permite executar uma consulta SQL (apenas SELECT) no banco de dados.
    
    Tabelas disponíveis:
    1. app_core.v_produtos (nome_produto, descricao, estoque_atual, estoque_minimo, ativo, data_validade)
    2. app_core.mv_movimentacao (produto_nome, quantidade, data_evento, valor_unitario, parceiro_origem, local_destino, tipo_movimento)
    
    Regras:
    - Retorne APENAS os dados estritamente necessários.
    - Sempre prefira usar as outras ferramentas antes desta.
    """
    
    query_upper = query_sql.upper()
    comandos_proibidos = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT", "REVOKE"]
    
    if any(cmd in query_upper for cmd in comandos_proibidos):
        return "Erro de Segurança: Apenas comandos SELECT são permitidos."
    
    if not query_upper.strip().startswith("SELECT"):
        return "Erro: A query deve obrigatoriamente começar com SELECT."
    
    if "LIMIT" not in query_upper:
        # Adicionar um LIMIT pra query
        query_sql = query_sql.strip().rstrip(";") + " LIMIT 20;"
        try:
            resultados = database.fetch_all(query=query_sql)
            
            if not resultados:
                return "A consulta foi executada com sucesso, mas não retornou nenhum resultado."
            
            return _wrap_rows(resultados, limit=20)
        
        except Exception as e:
            return f"Erro ao executar a query SQL: {str(e)}. Verifique a sintaxe, os nomes das colunas e tente novamente."
    
