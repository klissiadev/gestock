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

    # métodos auxiliares
    def _get_total_entrada(self, produto_id: int) -> int:
        result = self.repo.fetch_one(
            table="app_core.movimentacoes_entrada",
            columns=["COALESCE(SUM(quantidade), 0) AS total"],
            conditions={"produto_id": produto_id}
        )
        return result["total"] if result else 0

    def _get_total_saida(self, produto_id: int) -> int:
        result = self.repo.fetch_one(
            table="app_core.movimentacoes_saida",
            columns=["COALESCE(SUM(quantidade), 0) AS total"],
            conditions={"produto_id": produto_id}
        )
        return result["total"] if result else 0

    def _get_total_movimentacao(self, produto_id: int) -> dict:
        result = self.repo.fetch_one(
            table="app_core.movimentacoes_internas",
            columns=[
                "COALESCE(SUM(CASE WHEN tipo = 'producao' THEN quantidade END), 0) AS producao",
                "COALESCE(SUM(CASE WHEN tipo = 'consumo' THEN quantidade END), 0) AS consumo"
            ],
            conditions={"produto_id": produto_id}
        )
        return result or {"producao": 0, "consumo": 0}
 
    def _calculate_estoque_atual(self, produto_id: int) -> int:
        entrada = self._get_total_entrada(produto_id)
        saida = self._get_total_saida(produto_id)
        mov = self._get_total_movimentacao(produto_id)

        return entrada + mov["producao"] - mov["consumo"] - saida

    def _is_vencido(self, data_validade):
        if not data_validade:
            return False
        return data_validade < date.today()
    
    def _is_baixo_estoque(self, estoque_atual, estoque_minimo) -> bool:
        estoque_atual = estoque_atual or 0
        estoque_minimo = estoque_minimo or 0
        return estoque_atual <= estoque_minimo
  
    
    def _add_quotation_mark(self, value: str) -> str:
        return f"""{value}"""
    

    def see_product_table(
        self,
        direcao: str,
        order_by: str,
        search_term: str | None,
        categoria: str | None,
        apenas_baixo_estoque: bool,
        apenas_vencidos: bool
):
        COLUNAS_VALIDAS = [
            "id",
            "nome",
            "tipo",
            "descricao",
            "estoque_minimo",
            "data_validade"
        ]

        if order_by not in COLUNAS_VALIDAS:
            order_by = "nome"
        
        order_by = order_by or "nome"
        search_term = search_term.strip() if search_term else None

        conditions = {} 
        if categoria:
            conditions["tipo"] = categoria

        if not search_term:
            search_term = None

        produtos = self.repo.fetch_all(
            table="app_core.produtos", 
            columns=[ 
                "id",
                "nome",
                "tipo",
                "descricao",
                "estoque_minimo",
                "data_validade"
            ],
            conditions=conditions, 
            order_by=order_by, 
            direction=direcao, 
            search_term=search_term, 
            search_cols=["nome", "descricao"] 
        )

        
        resultado = [] 

        for produto in produtos: 
            estoque_atual = self._calculate_estoque_atual(produto["id"]) 
            vencido = self._is_vencido(produto["data_validade"])  
            baixo_estoque = self._is_baixo_estoque(
                estoque_atual,
                produto["estoque_minimo"]
            )

            if apenas_baixo_estoque and not baixo_estoque:
                continue
            if apenas_vencidos and not vencido:
                continue

            resultado.append({
                "id": produto["id"],
                "nome": produto["nome"],
                "tipo": produto["tipo"],
                "descricao": produto["descricao"],
                "estoque_atual": estoque_atual,
                "estoque_minimo": produto["estoque_minimo"],
                "baixo_estoque": baixo_estoque,
                "vencido": vencido
            })

        return resultado
    
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