# service/views_service
from backend.database.repository import Repository
import math


"""
    Serviço responsável por buscar Views armazenadas no banco de dados
    Para melhor desempenho -> Ainda em duvida sobre sistema de cache ou materialized view

    Por enquanto, vamos fazer consultas diretas pelo fetch_all()
"""

class view_service:
    def __init__(self, conn):
        self.repo = Repository(conn)
        
    def _calculate_low_stock_threshold(self, produto):
        """
        Calcula o limite de baixo estoque para um produto específico.
        Parâmetros:
        - produto (dict): Dicionário contendo os detalhes do produto, incluindo 'estoque_minimo'.

        Retorna:
        - float: O valor do limite de baixo estoque.
        """
        estoque_minimo = produto.get("estoque_minimo", 0)
        return math.floor(estoque_minimo * 1.2) 
    
    def _check_vencido(self, produto):
        """
        Verifica se um produto está vencido com base na data atual.
        Parâmetros:
        - produto (dict): Dicionário contendo os detalhes do produto, incluindo 'data_validade'.

        Retorna:
        - bool: True se o produto estiver vencido, False caso contrário.
        """
        from datetime import datetime

        data_validade = produto.get("data_validade")
        if data_validade:
            return data_validade < datetime.now().date()
        return False 
    
    def see_product_table(self, direcao: str, order: str, search_t: str, categoria: str, apenas_baixo_estoque: bool, apenas_vencidos: bool):
        """
        Responsável por buscar os produtos no banco de dados com base nos filtros fornecidos.
        Parâmetros:
        - direcao (str): A direção da ordenação (ascendente ou descendente).
        - order (str): O campo pelo qual ordenar os resultados.
        - search_t (str): Termo de busca para filtrar os produtos.
        - categoria (str): Categoria do produto para filtrar os resultados.
        - apenas_baixo_estoque (bool): Se verdadeiro, filtra apenas produtos com baixo estoque.
        - apenas_vencidos (bool): Se verdadeiro, filtra apenas produtos vencidos.

        Retorna:
        - Lista de produtos que correspondem aos critérios de busca e ordenação.
        """
        condicoes_db = {}

        if categoria:
            condicoes_db["categoria"] = categoria
            
        if apenas_baixo_estoque:
            # Busca todos os produtos primeiramente
            # Depois filtra os que estao com estoque baixo
            all_products = self.repo.fetch_all(
                table="Produto",
                conditions=condicoes_db,
                columns=["cod_produto", "nome", "descricao", "categoria", "valor_unitario", "estoque_atual", "estoque_minimo"],
                order_by=order,
                direction=direcao,
                search_term=search_t,
                search_cols=["nome", "descricao"],
            )
            
            low_stock_products = []
            for produto in all_products:
                low_stock_threshold = self._calculate_low_stock_threshold(produto)
                if produto["estoque_atual"] <= low_stock_threshold:
                    low_stock_products.append(produto)
            return low_stock_products
            
        if apenas_vencidos:
            all_products = self.repo.fetch_all(
                table="Produto",
                conditions=condicoes_db,
                columns=["cod_produto", "nome", "descricao", "categoria", "valor_unitario", "estoque_atual", "estoque_minimo", "data_validade"],
                order_by=order,
                direction=direcao,
                search_term=search_t,
                search_cols=["nome", "descricao"],
            )
            
            expired_products = []
            for produto in all_products:
                if self._check_vencido(produto):
                    #produto.pop("data_validade", None)  # Remove a data de validade do resultado final
                    expired_products.append(produto)
            return expired_products
            
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