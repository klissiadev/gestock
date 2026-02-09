from datetime import date, timedelta
from backend.database.repository import Repository


class AnalyticsService:
    def __init__(self, repo: Repository):
        self.repo = repo

    # =====================================================
    # KPIs GERAIS DE ESTOQUE
    # =====================================================

    def get_stock_kpis(self):
        estoque_total = self.repo.execute_query("""
            SELECT COALESCE(SUM(estoque_atual), 0) AS total
            FROM app_core.vw_product
        """)[0]

        baixo_estoque = self.repo.execute_query("""
            SELECT COUNT(*) AS count
            FROM app_core.vw_product
            WHERE estoque_atual <= estoque_minimo
        """)[0]

        vencidos = self.repo.execute_query("""
            SELECT COUNT(*) AS count
            FROM app_core.vw_product
            WHERE data_validade IS NOT NULL
            AND data_validade < CURRENT_DATE
        """)[0]

        return {
            "estoque_total": estoque_total["total"],
            "produtos_baixo_estoque": baixo_estoque["count"],
            "produtos_vencidos": vencidos["count"]
        }


    # =====================================================
    # ESTOQUE POR TIPO
    # =====================================================

    def get_stock_by_type(self):
        return self.repo.execute_query("""
            SELECT tipo,
                SUM(estoque_atual) AS estoque_total
            FROM app_core.vw_product
            GROUP BY tipo
            ORDER BY tipo
        """)


    # =====================================================
    # PRODUTOS CRÍTICOS
    # =====================================================

    def get_critical_products(self):
        return self.repo.execute_query("""
            SELECT
                p.id,
                p.nome,
                p.estoque_atual,
                p.estoque_minimo,
                COALESCE(SUM(m.quantidade), 0) AS total_saidas
            FROM app_core.vw_product p
            LEFT JOIN app_core.mv_movimentacao m
                ON m.produto_nome = p.nome
                AND m.tipo_movimento = 'SAIDA'
            WHERE p.estoque_atual <= p.estoque_minimo
            GROUP BY
                p.id,
                p.nome,
                p.estoque_atual,
                p.estoque_minimo
            ORDER BY total_saidas DESC
        """)


    # =====================================================
    # MOVIMENTAÇÃO POR PERÍODO (ENTRADAS X SAÍDAS)
    # =====================================================

    def get_movimentacao_por_periodo(self, start: date, end: date):
        return self.repo.execute_query("""
            SELECT
                DATE(data_evento) AS data,
                SUM(CASE WHEN tipo_movimento = 'ENTRADA' THEN quantidade ELSE 0 END) AS entradas,
                SUM(CASE WHEN tipo_movimento = 'SAIDA' THEN quantidade ELSE 0 END) AS saidas
            FROM app_core.mv_movimentacao
            WHERE data_evento BETWEEN %s AND %s
            GROUP BY DATE(data_evento)
            ORDER BY data
        """, (start, end))


    # =====================================================
    # KPIs FINANCEIROS
    # =====================================================

    def get_financial_kpis(self):
        compras = self.repo.execute_query("""
            SELECT COALESCE(SUM(quantidade * valor_unitario), 0) AS total
            FROM app_core.mv_movimentacao
            WHERE tipo_movimento = 'ENTRADA'
        """)[0]

        vendas = self.repo.execute_query("""
            SELECT COALESCE(SUM(quantidade * valor_unitario), 0) AS total
            FROM app_core.mv_movimentacao
            WHERE tipo_movimento = 'SAIDA'
        """)[0]

        return {
            "valor_compras": compras["total"],
            "valor_vendas": vendas["total"],
            "margem_bruta_estimada": vendas["total"] - compras["total"]
        }


    # =====================================================
    # PRODUTOS MAIS VENDIDOS
    # =====================================================

    def get_top_selling_products(self, limit: int = 5):
        return self.repo.execute_query("""
            SELECT
                produto_nome AS nome,
                SUM(quantidade) AS total_vendido,
                SUM(quantidade * valor_unitario) AS faturamento
            FROM app_core.mv_movimentacao
            WHERE tipo_movimento = 'SAIDA'
            GROUP BY produto_nome
            ORDER BY total_vendido DESC
            LIMIT %s
        """, (limit,))


    # =====================================================
    # PRODUTOS PRÓXIMOS DO VENCIMENTO
    # =====================================================

    def get_products_near_expiration(self, days: int = 30):
        limite = date.today() + timedelta(days=days)

        return self.repo.fetch_all("""
            SELECT id, nome, data_validade
            FROM app_core.vw_product
            WHERE data_validade IS NOT NULL
              AND data_validade BETWEEN CURRENT_DATE AND %s
            ORDER BY data_validade
        """, (limite,))

    # =====================================================
    # PRODUÇÃO / CONSUMO (MOVIMENTAÇÃO INTERNA)
    # =====================================================

    def get_production_summary(self):
        return self.repo.fetch_all("""
            SELECT
                tipo_movimento,
                SUM(quantidade) AS total
            FROM app_core.mv_movimentacao
            WHERE tipo_movimento = 'INTERNA'
            GROUP BY tipo_movimento
        """)

    # =====================================================
    # GIRO DE ESTOQUE (SIMPLIFICADO)
    # =====================================================

    def get_stock_turnover(self, start: date, end: date):
        saidas = self.repo.fetch_one("""
            SELECT COALESCE(SUM(quantidade), 0) AS total
            FROM app_core.mv_movimentacao
            WHERE tipo_movimento = 'SAIDA'
              AND data_evento BETWEEN %s AND %s
        """, (start, end))

        estoque_medio = self.repo.fetch_one("""
            SELECT AVG(estoque_atual) AS medio
            FROM app_core.vw_product
        """)

        giro = 0
        if estoque_medio["medio"] and estoque_medio["medio"] > 0:
            giro = saidas["total"] / estoque_medio["medio"]

        return {
            "saidas_periodo": saidas["total"],
            "estoque_medio": estoque_medio["medio"],
            "giro_estoque": round(giro, 2)
        }

