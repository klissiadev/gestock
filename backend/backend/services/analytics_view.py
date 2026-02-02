from datetime import date, timedelta
from backend.database.repository import Repository


class AnalyticsService:
    def __init__(self, repo: Repository):
        self.repo = repo

    # =====================================================
    # KPIs (indicadores chaves de desempenho)  GERAIS DE ESTOQUE
    # =====================================================

    def get_stock_kpis(self):
        """
        KPIs principais para cards do dashboard
        retorna:
        - estoque total atual
        - quantidade de produtos a abaixo do estoque
        - quantidade de produtos vencidos

        """
        estoque_total = self.repo.fetch_one("""
            SELECT COALESCE(SUM(estoque_atual), 0) AS total
            FROM app_core.v_produtos
        """)

        baixo_estoque = self.repo.fetch_one("""
            SELECT COUNT(*) AS count
            FROM app_core.v_produtos
            WHERE estoque_atual <= estoque_minimo
        """)

        vencidos = self.repo.fetch_one("""
            SELECT COUNT(*) AS count
            FROM app_core.v_produtos
            WHERE data_validade IS NOT NULL
              AND data_validade < CURRENT_DATE
        """)

        return {
            "estoque_total": estoque_total["total"],
            "produtos_baixo_estoque": baixo_estoque["count"],
            "produtos_vencidos": vencidos["count"]
        }

    # =====================================================
    # ESTOQUE POR TIPO (MP, SA, PA)
    # =====================================================

    def get_stock_by_type(self):
        """
        Retorna a quantidade de estoque por cada tipo de produto
        """
        return self.repo.fetch_all("""
            SELECT p.tipo,
                   SUM(v.estoque_atual) AS estoque_total
            FROM app_core.v_produtos v
            JOIN produtos p ON p.id = v.produto_id
            GROUP BY p.tipo
            ORDER BY p.tipo
        """)

    # =====================================================
    # PRODUTOS CRÍTICOS
    # =====================================================

    def get_critical_products(self):
        """
        Produtos abaixo do mínimo com alta saída
        """
        return self.repo.fetch_all("""
            SELECT p.id,
                   p.nome,
                   v.estoque_atual,
                   p.estoque_minimo,
                   COALESCE(SUM(s.quantidade), 0) AS total_saidas
            FROM app_core.v_produtos p
            JOIN view_produto_estoque v ON v.produto_id = p.id
            LEFT JOIN saida s ON s.produto_id = p.id
            GROUP BY p.id, p.nome, v.estoque_atual, p.estoque_minimo
            HAVING v.estoque_atual <= p.estoque_minimo
            ORDER BY total_saidas DESC
        """)

    # =====================================================
    # MOVIMENTAÇÃO POR PERÍODO (ENTRADAS X SAÍDAS)
    # =====================================================

    def get_movimentacao_por_periodo(self, start: date, end: date):
        """
        Série temporal de entradas e saídas
        """
        return self.repo.fetch_all("""
            SELECT data, SUM(entradas) AS entradas, SUM(saidas) AS saidas
            FROM (
                SELECT data_de_compra AS data,
                       SUM(quantidade) AS entradas,
                       0 AS saidas
                FROM entrada
                WHERE data_de_compra BETWEEN %s AND %s
                GROUP BY data_de_compra

                UNION ALL

                SELECT data_de_venda AS data,
                       0 AS entradas,
                       SUM(quantidade) AS saidas
                FROM saida
                WHERE data_de_venda BETWEEN %s AND %s
                GROUP BY data_de_venda
            ) t
            GROUP BY data
            ORDER BY data
        """, (start, end, start, end))

    # =====================================================
    # KPIs FINANCEIROS
    # =====================================================

    def get_financial_kpis(self):
        """
        Indicadores financeiros básicos
        """
        compras = self.repo.fetch_one("""
            SELECT COALESCE(SUM(quantidade * preco_de_compra), 0) AS total
            FROM entrada
        """)

        vendas = self.repo.fetch_one("""
            SELECT COALESCE(SUM(quantidade * preco_de_venda), 0) AS total
            FROM saida
        """)

        return {
            "valor_compras": compras["total"],
            "valor_vendas": vendas["total"],
            "margem_bruta_estimada": vendas["total"] - compras["total"]
        }

    # =====================================================
    # PRODUTOS MAIS VENDIDOS
    # =====================================================

    def get_top_selling_products(self, limit: int = 5):
        return self.repo.fetch_all("""
            SELECT p.nome,
                   SUM(s.quantidade) AS total_vendido,
                   SUM(s.quantidade * s.preco_de_venda) AS faturamento
            FROM saida s
            JOIN produtos p ON p.id = s.produto_id
            GROUP BY p.nome
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
            FROM produtos
            WHERE data_validade IS NOT NULL
              AND data_validade BETWEEN CURRENT_DATE AND %s
            ORDER BY data_validade
        """, (limite,))

    # =====================================================
    # PRODUÇÃO E CONSUMO (MOVIMENTAÇÕES INTERNAS)
    # =====================================================

    def get_production_summary(self):
        """
        Resumo de consumo e produção
        """
        return self.repo.fetch_all("""
            SELECT tipo,
                   SUM(quantidade) AS total
            FROM movimentacoes_internas
            GROUP BY tipo
        """)

    # =====================================================
    # GIRO DE ESTOQUE (SIMPLIFICADO)
    # =====================================================

    def get_stock_turnover(self, start: date, end: date):
        """
        Giro = saídas / estoque médio
        """
        saidas = self.repo.fetch_one("""
            SELECT COALESCE(SUM(quantidade), 0) AS total
            FROM saida
            WHERE data_de_venda BETWEEN %s AND %s
        """, (start, end))

        estoque_medio = self.repo.fetch_one("""
            SELECT AVG(estoque_atual) AS medio
            FROM view_produto_estoque
        """)

        giro = 0
        if estoque_medio["medio"] and estoque_medio["medio"] > 0:
            giro = saidas["total"] / estoque_medio["medio"]

        return {
            "saidas_periodo": saidas["total"],
            "estoque_medio": estoque_medio["medio"],
            "giro_estoque": round(giro, 2)
        }
