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
            
        all_products = self.repo.fetch_all(
                table="Produto",
                conditions=condicoes_db,
                columns=["cod_produto", "nome", "descricao", "categoria", "valor_unitario", "estoque_atual", "estoque_minimo"],
                order_by=order,
                direction=direcao,
                search_term=search_t,
                search_cols=["nome", "descricao"],
                )
        
        if not apenas_baixo_estoque and not apenas_vencidos:
            # Remover data_validade se não estiver filtrando por vencidos
            for p in all_products:
                p.pop("data_validade", None)
            return all_products

        filtered_products = []
        for produto in all_products:
            low_stock_threshold = self._calculate_low_stock_threshold(produto)
            is_low_stock = produto["estoque_atual"] <= low_stock_threshold     # Verifica se o produto está com baixo estoque
            is_expired = self._check_vencido(produto)                          # Verifica se o produto está vencido
            
            # Aplicação dos filtros adicionais
            if apenas_baixo_estoque and not is_low_stock: 
                continue
            if apenas_vencidos and not is_expired:
                continue
            
            if "data_validade" in produto and not apenas_vencidos:
                produto.pop("data_validade", None)
            filtered_products.append(produto) 
        return filtered_products

        
    def see_movimentacao_table(self):
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
        return self.repo.fetch_all(
                    table="Movimentacao",
                    direction="DESC"
                    )

