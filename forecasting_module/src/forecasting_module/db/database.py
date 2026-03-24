# forecasting/db/repository.py
import psycopg
from psycopg.rows import dict_row
from datetime import date, datetime
from typing import List, Tuple
from forecasting_module.schemas.models import FieldSaida

class Repository:
    def __init__(self, conexao: psycopg.Connection):
        self.conn = conexao

    def buscar_dados_anomalia(self, data_corte: date):
        query = """
            SELECT *
            FROM app_core.vw_anomaly_input
            WHERE date >= %s
            ORDER BY date ASC;
        """

        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (data_corte,))
                return cursor.fetchall()

        except Exception as e:
            print(f"Erro ao buscar dados de anomalia: {e}")
            raise e
    
    
if __name__ == '__main__':
    repo = Repository(psycopg.connect("postgresql://neondb_owner:npg_ifdqC3DUy0aG@ep-autumn-darkness-ac5hhgfe.sa-east-1.aws.neon.tech/neondb"))
    
    
    print(repo.buscar_historico_vendas(produto_id=32, 
                                      data_corte=datetime.strptime("01/01/2026", '%d/%m/%Y').date()))