# service/views_service
from datetime import date
from backend.database.repository import Repository
import math


"""
    Serviço responsável por buscar Views armazenadas no banco de dados
    Para melhor desempenho -> Ainda em duvida sobre sistema de cache ou materialized view

    Por enquanto, vamos fazer consultas diretas pelo fetch_all()

    # TODO: refatorar cálculo de estoque para query agregada ou view (evitar N+1)

"""

class view_service:
    def __init__(self, conn):
        self.repo = Repository(conn)
    
    def _add_quotation_mark(self, value: str) -> str:
        return f"""{value}"""
    

    def see_product_table(
        self,
        direcao: str,
        order_by: str,
        search_term: str | None,
        tipo: str | None,
        apenas_baixo_estoque: bool | None,
        apenas_vencidos: bool  | None
    ):
        COLUNAS_VALIDAS = [
            "id", "nome", "tipo", "descricao", "estoque_atual",
            "estoque_minimo", "baixo_estoque", "vencido", 
            "data_validade", "ativo"
        ]

        if order_by not in COLUNAS_VALIDAS:
            order_by = "nome"
        
        order_by = order_by or "nome"
        search_term = search_term.strip() if search_term else None

        conditions = {} 
        if tipo:
            conditions["tipo"] = tipo
        if apenas_baixo_estoque:
            conditions["baixo_estoque"] = True
        if apenas_vencidos:
            conditions["vencido"] = True
        

        if not search_term:
            search_term = None

        produtos = self.repo.fetch_all(
            table="app_core.vw_product", 
            columns=COLUNAS_VALIDAS,
            conditions=conditions, 
            order_by=order_by, 
            direction=direcao, 
            search_term=search_term, 
            search_cols=["nome", "descricao"] 
        )

        return produtos
    
    def see_movimentacao_table(self, direcao: str, order_by: str, search_term: str | None):
        return self.repo.fetch_all(
            table="movimentacoes_internas",
            columns=[
                "id",
                "produto_id",
                "ordem_de_producao",
                "tipo",
                "quantidade",
                "origem",
                "destino",
                "data"
            ],
            order_by=order_by,
            direction=direcao,
            search_term=search_term,
            search_cols=["ordem_de_producao", "origem", "destino"]
        )
    

def testes():
    import psycopg2
    from psycopg2.extras import RealDictCursor
    import os
    from dotenv import load_dotenv
    from backend.models.product_item import ProductSchema # Importe seu modelo
    
    load_dotenv()

    conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5432"),
            dbname=os.getenv("PG_DATABASE", "meubanco"),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "postgres"),
            cursor_factory=RealDictCursor,
            connect_timeout=5)
    
    try:
        view = view_service(conn) 
        
        print("--- Executando busca na View ---")
        resultados_brutos = view.see_product_table(
            direcao="ASC", 
            order_by="nome", 
            tipo=None, 
            search_term=None, 
            apenas_baixo_estoque=True, 
            apenas_vencidos=None
        )

        print(f"Total de registros encontrados: {len(resultados_brutos)}")

        # 2. Testando a validação do Pydantic (Simulando o que o FastAPI faz)
        print("\n--- Validando com Pydantic ---")
        for item in resultados_brutos[:2]: # Testa apenas os 2 primeiros
            # Converte o dicionário bruto em um objeto Pydantic
            produto_validado = ProductSchema(**item)
            
            # O .model_dump_json() simula exatamente o que o React vai receber
            # Note como a data vira string automaticamente aqui!
            print(f"Produto: {produto_validado.nome}")
            print(f"JSON de saída: {produto_validado.model_dump_json()}")
            print("-" * 20)

    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    testes()

'''
Estrutura atual das tabelas:

tabela produtos:
- nome 
- tipo(MP, SA e PA)
- descricao
- estoque_minimo
- data_validade

tabela de entrada:
- produto_id
- quantidade 
- data_de_compra
- preco_de_compra
- fornecedor

tabela de movimentacoes internas:
- produto_id
- ordem_de_producao
- tipo (consumo ou producao)
- quantidade
- origem
- destino
- data

tabela de saida:
- produto_id
- quantidade 
- data_de_venda
- preco_de_venda
- cliente   

'''