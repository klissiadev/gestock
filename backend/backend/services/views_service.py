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
        """
        Responsável por buscar os produtos no banco de dados com base nos filtros fornecidos.
        Parâmetros:
        - direcao (str): A direção da ordenação (ascendente ou descendente).
        - order (str): O campo pelo qual ordenar os resultados.
        - search_t (str): Termo de busca para filtrar os produtos.
        - categoria (str): Categoria do produto para filtrar os resultados.

        Retorna:
        - Lista de produtos que correspondem aos critérios de busca e ordenação.
        """
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
        
    def see_movimentacao_table(self, direcao:str, order:str, search_t:str, tipo_movimentacao:str):
        """
        Responsável por buscar as movimentações de estoque no banco de dados com base nos filtros fornecidos.
        Parâmetros:
        - direcao (str): A direção da ordenação (ascendente ou descendente).
        - order (str): O campo pelo qual ordenar os resultados.
        - search_t (str): Termo de busca para filtrar as movimentações.
        - tipo_movimentacao (str): Tipo de movimentação para filtrar os resultados.
        
        Retorna:
        - Lista de movimentações que correspondem aos critérios de busca e ordenação.
        """
        condicoes_db = {}

        if tipo_movimentacao:
            condicoes_db["tipo_movimentacao"] = tipo_movimentacao

        return self.repo.fetch_all(
                table="Movimentacao_Estoque",
                conditions=condicoes_db,
                columns=["cod_movimentacao", "cod_produto", "quantidade", "tipo_movimentacao", "data_hora", "responsavel"],
                order_by=order,
                direction=direcao,
                search_term=search_t,
                search_cols=["cod_produto", "responsavel"],
                )