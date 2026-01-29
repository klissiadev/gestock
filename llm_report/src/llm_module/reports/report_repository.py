from datetime import date, timedelta
from typing import Any, Dict, List

from llm_module.utils.postgres_client import PostgresClient


class ReportRepository:
    """
    Camada responsável por acessar o banco de dados.
    Aqui ficam apenas consultas SQL (preferencialmente em views).
    """

    def __init__(self):
        self.db = PostgresClient()

    # -------------------------
    # Estoque
    # -------------------------

    def get_estoque_baixo(self, limite: int | None = None) -> List[Dict[str, Any]]:
        """
        Produtos cujo estoque atual é menor ou igual ao estoque mínimo.
        """
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

    def get_validade_proxima(self, dias: int) -> List[Dict[str, Any]]:
        """
        Produtos com data de validade dentro dos próximos X dias.
        """
        data_limite = (date.today() + timedelta(days=dias)).isoformat()

        sql = f"""
            SELECT
                nome_produto,
                descricao,
                estoque_atual,
                estoque_minimo,
                data_validade
            FROM app_core.v_produtos
            WHERE data_validade IS NOT NULL
              AND data_validade <= '{data_limite}'
            ORDER BY data_validade, nome_produto
        """

        return self.db.fetch_all(query=sql)

    # -------------------------
    # Giro de produtos
    # -------------------------

    def get_produtos_sem_giro(self, dias: int) -> List[Dict[str, Any]]:
        """
        Produtos sem qualquer movimentação (entrada ou saída)
        nos últimos X dias.
        """
        data_limite = (date.today() - timedelta(days=dias)).isoformat()

        sql = f"""
            SELECT
                p.nome_produto,
                p.descricao,
                p.estoque_atual,
                MAX(m.data_movimentacao) AS ultima_movimentacao
            FROM app_core.v_produtos p
            LEFT JOIN app_core.v_movimentacao m
                ON m.nome_produto = p.nome_produto
            GROUP BY
                p.nome_produto,
                p.descricao,
                p.estoque_atual
            HAVING
                MAX(m.data_movimentacao) IS NULL
                OR MAX(m.data_movimentacao) < '{data_limite}'
            ORDER BY ultima_movimentacao NULLS FIRST, p.nome_produto
        """

        return self.db.fetch_all(query=sql)

    # -------------------------
    # Movimentações
    # -------------------------

    def get_movimentacao_periodo(self, data_inicio: str, data_fim: str) -> List[Dict[str, Any]]:
        """
        Todas as movimentações dentro de um período.
        """
        sql = f"""
            SELECT
                nome_produto,
                tipo_movimentacao,
                quantidade,
                entidade,
                data_movimentacao
            FROM app_core.v_movimentacao
            WHERE data_movimentacao BETWEEN '{data_inicio}' AND '{data_fim}'
            ORDER BY data_movimentacao DESC
        """

        return self.db.fetch_all(query=sql)

    def get_entradas_saidas(self, data_inicio: str, data_fim: str) -> Dict[str, Any]:
        """
        Resumo de entradas e saídas por produto no período.
        """
        sql = f"""
            SELECT
                nome_produto,
                tipo_movimentacao,
                SUM(quantidade) AS total_quantidade
            FROM app_core.v_movimentacao
            WHERE data_movimentacao BETWEEN '{data_inicio}' AND '{data_fim}'
            GROUP BY nome_produto, tipo_movimentacao
            ORDER BY nome_produto
        """

        rows = self.db.fetch_all(query=sql)

        resumo: Dict[str, Dict[str, int]] = {}
        for row in rows:
            produto = row["nome_produto"]
            tipo = row["tipo_movimentacao"]
            qtd = row["total_quantidade"]

            if produto not in resumo:
                resumo[produto] = {"entrada": 0, "saida": 0}

            resumo[produto][tipo] = qtd

        return resumo
