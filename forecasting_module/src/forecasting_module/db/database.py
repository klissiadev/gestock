# forecasting/db/repository.py
import psycopg
from psycopg.rows import dict_row
from datetime import date, datetime
from typing import List, Tuple
from forecasting_module.schemas.models import FieldSaida

class Repository:
    def __init__(self, conexao: psycopg.AsyncConnection):
        self.conn = conexao

    async def buscar_historico_vendas(self, produto_id: int, data_corte: date) -> List[FieldSaida]:
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
            async with self.conn.cursor(row_factory=dict_row) as cursor:
                await cursor.execute(query, (produto_id, data_corte))
                registros = await cursor.fetchall()
                
                movimentacoes_validadas = [FieldSaida(**row) for row in registros]
                
                return movimentacoes_validadas
                
        except Exception as e:
            print(f"Erro ao buscar histórico do produto {produto_id}: {e}")
            raise e
    
    
    async def necessidade_compra(self):
        query_calculo = """
            WITH ProdutosFaltantes AS (
                SELECT 
                    id AS produto_final_id,
                    ((estoque_minimo * 2) - estoque_atual) AS deficit_fabricacao
                FROM 
                    app_core.vw_product
                WHERE 
                    estoque_atual <= estoque_minimo AND ativo = true AND tipo = 'Produto Acabado'
            )

            SELECT 
                ft.materia_prima_id,
                mp.nome AS nome_materia_prima,
                SUM(pf.deficit_fabricacao * ft.quantidade_necessaria) AS quantidade_sugerida_compra
            FROM 
                ProdutosFaltantes pf
            JOIN 
                app_core.ficha_tecnica ft ON pf.produto_final_id = ft.produto_final_id
            JOIN 
                app_core.vw_product mp ON ft.materia_prima_id = mp.id 
            GROUP BY 
                ft.materia_prima_id, 
                mp.nome;
            """
        try:
            async with self.conn.cursor(row_factory=dict_row) as cursor:
                await cursor.execute(query_calculo)
                registros = await cursor.fetchall()
                
                return registros
                
        except Exception as e:
            print(f"Erro ao buscar histórico do produto {produto_id}: {e}")
            raise e
        
    async def buscar_historico_saidas(self, produto_id: int):
        query = """
            SELECT 
                TO_CHAR(DATE_TRUNC('month', data_de_venda), 'YYYY-MM') AS mes,
                SUM(quantidade) AS demanda_real
            FROM 
                app_core.movimentacoes_saida
            WHERE 
                produto_id = %s
            GROUP BY 
                DATE_TRUNC('month', data_de_venda)
            ORDER BY 
                DATE_TRUNC('month', data_de_venda) ASC;
        """
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, (produto_id,))
                registros = await cursor.fetchall()
                return registros
        except Exception as e:
            print(f"Erro ao buscar histórico de saídas: {e}")
            raise e
      
        
    async def listar_produtos_com_vendas(self):
        query = """
            SELECT 
                p.id, 
                p.nome
            FROM 
                app_core.vw_product p
            WHERE 
                p.tipo = 'Produto Acabado' 
                AND p.ativo = true
                AND EXISTS (
                    -- O banco só lista o produto se achar pelo menos 1 saída dele
                    SELECT 1 
                    FROM app_core.movimentacoes_saida v
                    WHERE v.produto_id = p.id
                )
            ORDER BY 
                p.nome;
        """
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(query)
                return await cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar produtos para o dropdown: {e}")
            raise e

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
