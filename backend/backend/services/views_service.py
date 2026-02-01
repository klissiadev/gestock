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
        apenas_vencidos: bool | None
    ):
        COLUNAS_VALIDAS = [
            "id", "nome", "tipo", "descricao", "estoque_atual",
            "estoque_minimo", "baixo_estoque", "vencido", 
            "data_validade", "ativo"
        ]

        if order_by not in COLUNAS_VALIDAS:
            order_by = "id"

        search_term = search_term.strip() if search_term and search_term.strip() else None
        tipo = tipo.strip() if tipo and tipo.strip() else None

        conditions = {
            k: v for k, v in {
                "tipo": tipo,
                "baixo_estoque": True if apenas_baixo_estoque else None,
                "vencido": True if apenas_vencidos else None
            }.items() if v is not None
        }

        return self.repo.fetch_all(
            table="app_core.vw_product", 
            columns=COLUNAS_VALIDAS,
            conditions=conditions, 
            order_by=order_by, 
            direction=direcao, 
            search_term=search_term, 
            search_cols=["nome", "descricao"] 
        )
    
    def see_transaction_table(self, direcao: str, order_by: str, search_term: str | None):
        COLUNAS_VIEW = [
            "unique_id", "produto_nome", "quantidade", "data_evento",
            "valor_unitario", "parceiro_origem", "local_destino",
            "tipo_movimento", "created_at"
        ]

        if order_by not in COLUNAS_VIEW:
            order_by = "unique_id" 

        search_term = search_term.strip() if search_term else None

        BUSCA_EM = ["produto_nome", "parceiro_origem", "local_destino", "tipo_movimento"]

        return self.repo.fetch_all(
            table="app_core.mv_movimentacao",
            columns=COLUNAS_VIEW,
            order_by=order_by,
            direction=direcao,
            search_term=search_term,
            search_cols=BUSCA_EM
        )
    

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