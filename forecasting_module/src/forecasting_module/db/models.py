# db/repository.py
import psycopg
from datetime import date

def buscar_historico_vendas(conexao: psycopg.Connection, produto_id: int, data_corte: date):
    """
    Busca as movimentações de saída de um Produto a partir de uma data específica.
    Retorna uma lista de tuplas com os resultados.
    """
    query = """
        SELECT 
            id, 
            produto_id, 
            quantidade, 
            data_de_venda, 
            preco_de_venda, 
            fornecedor, 
            importado_em
        FROM movimentacoes_saida
        WHERE produto_id = %s AND data_de_venda >= %s
        ORDER BY data_de_venda ASC;
    """
    
    with conexao.cursor() as cursor:
        cursor.execute(query, (e_produto_id, data_corte))
        registros = cursor.fetchall()
        
    return registros