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
    
def _normalize_table_info(information: list[dict]) -> dict:
    """
    Normaliza a informação das tabelas para um formato mais amigável.
    """
    esquema = {}
    for row in information:
        table_name = row['table_name']
        column_name = row['column_name']
        data_type = row['data_type']
        
        if table_name not in esquema:
            esquema[table_name] = []
        
        esquema[table_name].append(f"{column_name} ({data_type})")
    
    return esquema


@tool
def tool_consultar_estoque(query_sql: str) -> dict:
    """
    Executa uma consulta SQL no banco de dados de produtos.
    Use esta ferramenta para filtrar, ordenar ou buscar informações específicas.
    A tabela disponível é: app_core.v_produtos
    Colunas:
        - id (int)
        - nome (string)
        - descricao (string)
        - data_validade (date)
    Exemplo: SELECT nome FROM app_core.v_produtos ORDER BY data_validade ASC LIMIT 1;
    """
    # Importante: Valide se a query é apenas SELECT para segurança básica
    if not query_sql.strip().upper().startswith("SELECT"):
        return {"erro": "Apenas consultas de leitura (SELECT) são permitidas."}
    try:
        rows = database.fetch_all(query_sql)
        return _wrap_rows(rows)
    except Exception as e:
        return {"erro": f"Erro na query SQL: {str(e)}"}

# AINDA EM DESENVOLVIMENTO E FORA DE USO
def tool_descobrir_tabelas():
    """
    Retorna a lista de tabelas disponíveis para consulta no banco de dados, com suas respectivas colunas.
    """
    columns = []
    
    query_table = "SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema = 'app_core' ORDER BY table_name;"
    table_names = database.fetch_all(query_table)   
    table_names = _normalize_table_info(table_names)
    
    return table_names