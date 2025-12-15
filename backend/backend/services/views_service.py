# service/views_service
from backend.database.repository import Repository
from backend.database.base import get_connection
from fastapi import APIRouter, Depends

"""
    Serviço responsável por buscar Views armazenadas no banco de dados
    Para melhor desempenho -> Ainda em duvida sobre sistema de cache ou materialized view

    Por enquanto, vamos fazer consultas diretas pelo fetch_all()
"""

class view_service:
    def __init__(self, conn):
        self.repo = Repository(conn)
    
    def see_product_table(self, direcao: str, order: str, search_t: str, categoria: str):
        condicoes_db = {}

        if categoria:
            condicoes_db["categoria"] = categoria

        return self.repo.fetch_all(
                table="Produto",
                conditions=condicoes_db,
                columns=["cod_produto", "nome", "descricao", "categoria", "valor_unitario", "estoque_atual", "estoque_minimo"],
                order_by=order,
                direction=direcao,
                search_term=search_t,
                search_cols=["nome", "descricao"],
                )