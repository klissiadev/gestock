from datetime import date, timedelta
from typing import Any, Dict, List

from llm_module.utils.postgres_client import PostgresClient


class ReportRepository:
    """
    Camada responsável por acessar o banco de dados.
    Apenas consultas SQL.
    """

    def __init__(self):
        self.db = PostgresClient()

    # =====================================================
    # RELATÓRIO – ESTOQUE BAIXO
    # =====================================================

    def get_estoque_baixo(self, limite: int | None = None) -> List[Dict[str, Any]]:
        sql = """
            SELECT
                nome_produto,
                descricao,
                estoque_atual,
                estoque_minimo
            FROM app_core.v_produtos
            WHERE estoque_atual <= estoque_minimo
            ORDER BY (estoque_minimo - estoque_atual) DESC, nome_produto
        """

        if limite:
            sql += f" LIMIT {int(limite)}"

        return self.db.fetch_all(query=sql)

    # =====================================================
    # RELATÓRIO – INVENTÁRIO / SALDO DE ESTOQUE
    # =====================================================

    def get_inventario(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT
                nome_produto,
                descricao,
                estoque_atual,
                estoque_minimo,
                data_validade,
                ativo
            FROM app_core.v_produtos
            ORDER BY nome_produto
        """

        return self.db.fetch_all(query=sql)

    # =====================================================
    # RELATÓRIO – VALIDADE PRÓXIMA
    # =====================================================

    def get_validade_proxima(self, dias: int) -> List[Dict[str, Any]]:
        data_limite = (date.today() + timedelta(days=dias)).isoformat()

        sql = f"""
            SELECT
                nome_produto,
                descricao,
                estoque_atual,
                data_validade
            FROM app_core.v_produtos
            WHERE data_validade IS NOT NULL
              AND data_validade <= '{data_limite}'
            ORDER BY data_validade
        """

        return self.db.fetch_all(query=sql)

    # =====================================================
    # RELATÓRIO – PRODUTOS SEM GIRO
    # =====================================================

    def get_produtos_sem_giro(self, data_limite: date):

        sql = """
            SELECT
                nome_produto,
                ultima_movimentacao
            FROM app_core.v_ultima_movimentacao_produto
            WHERE ultima_movimentacao IS NULL
            OR ultima_movimentacao > %s
            ORDER BY ultima_movimentacao NULLS FIRST
        """

        return self.db.fetch_all(query=sql, params=[data_limite])

    # =====================================================
    # RELATÓRIO – MOVIMENTAÇÕES NO PERÍODO
    # =====================================================

    def get_movimentacao_periodo(
        self,
        data_inicio: str,
        data_fim: str
    ) -> List[Dict[str, Any]]:

        sql = """
            SELECT
                nome_produto,
                quantidade,
                entidade,
                data_movimentacao,
                tipo_movimentacao AS tipo_movimentacao
            FROM app_core.v_movimentacao
            WHERE data_movimentacao BETWEEN %s AND %s
            ORDER BY data_movimentacao DESC
        """

        return self.db.fetch_all(sql, (data_inicio, data_fim))

    # =====================================================
    # RELATÓRIO – ENTRADAS E SAÍDAS
    # =====================================================

    def get_entradas_saidas(
        self,
        data_inicio: str,
        data_fim: str
    ):

        sql = """
            SELECT
                nome_produto,
                entidade,
                tipo_movimentacao AS tipo_movimentacao,
                SUM(quantidade) AS total_quantidade
            FROM app_core.v_movimentacao
            WHERE data_movimentacao BETWEEN %s AND %s
            GROUP BY
                nome_produto,
                entidade,
                tipo_movimentacao
            ORDER BY nome_produto
        """

        return self.db.fetch_all(query=sql, params=(data_inicio, data_fim))

    # =====================================================
    # RELATÓRIO – GIRO DE ESTOQUE
    # =====================================================

    def get_giro_estoque(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT
                nome_produto,
                total_entrada,
                total_saida,
                total_movimentacoes
            FROM app_core.v_giro_estoque
            ORDER BY total_movimentacoes DESC
        """

        return self.db.fetch_all(query=sql)

    
    # =====================================================
    # RELATÓRIO – SALDO DE ESTOQUE
    # =====================================================
    def get_saldo_estoque(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT
                nome_produto,
                estoque_atual,
                estoque_minimo
            FROM app_core.v_produtos
            ORDER BY nome_produto
        """

        return self.db.fetch_all(query=sql)
    
    # =====================================================
    # RELATÓRIO – PRODUTOS CUSTO
    # =====================================================
    def get_produtos_custo(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT
                produto_id,
                nome_produto,
                estoque_atual,
                custo_medio,
                valor_total
            FROM app_core.v_produtos_custo
            ORDER BY valor_total DESC
        """

        return self.db.fetch_all(query=sql)

