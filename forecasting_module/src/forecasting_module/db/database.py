# forecasting/db/repository.py
import psycopg
from psycopg.rows import dict_row
from datetime import date, datetime
from typing import List, Tuple
from forecasting_module.schemas.models import FieldSaida

class Repository:
    def __init__(self, conexao: psycopg.Connection):
        self.conn = conexao

    def buscar_historico_vendas(self, produto_id: int, data_corte: date) -> List[FieldSaida]:
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
                preco_de_venda
            FROM app_core.movimentacoes_saida
            WHERE produto_id = %s AND data_de_venda >= %s
            ORDER BY data_de_venda ASC;
        """
        
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (produto_id, data_corte))
                registros = cursor.fetchall()
                
                movimentacoes_validadas = [FieldSaida(**row) for row in registros]
                
                return movimentacoes_validadas
                
        except Exception as e:
            print(f"Erro ao buscar histórico do produto {produto_id}: {e}")
            raise e
    
    
if __name__ == '__main__':
    repo = Repository(psycopg.connect("postgresql://neondb_owner:npg_ifdqC3DUy0aG@ep-autumn-darkness-ac5hhgfe.sa-east-1.aws.neon.tech/neondb"))
    
    
    print(repo.buscar_historico_vendas(produto_id=32, 
                                      data_corte=datetime.strptime("01/01/2026", '%d/%m/%Y').date()))