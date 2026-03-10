from datetime import date, timedelta
from backend.database.repository import Repository


'''
Os dados gerados até o momento são:

- Estoque atual (todos os produtos)
- Estoque atual de matéria prima
- Estoque atual de produtos Semi-Acabados
- Estoque atual de produtos acabados

- top produtos acabados mais vendidos (leva em consideração o mês)
- itens críticos
- quantidade de itens vendidos em cada mês (leva em consideração um ano)

'''



class AnalyticsService:
    def __init__(self, repo: Repository):
        self.repo = repo


    '''
    # =====================================================
    # KPIs GERAIS DE ESTOQUE
    # =====================================================

    calcula:
    - estoque total geral
    - qtd de produtos com baixo estoque geral
    - qtd de produtos vencidos geral

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

    '''

    # =====================================================
    # KPIs FINANCEIROS
    # =====================================================
    
    def get_financial_kpis_por_mes(self, start: date, end: date):
        return self.repo.execute_query("""
            SELECT
                DATE_TRUNC('month', data_evento) AS mes,
                SUM(CASE WHEN tipo_movimento = 'ENTRADA'
                        THEN quantidade * valor_unitario ELSE 0 END) AS valor_compras,
                SUM(CASE WHEN tipo_movimento = 'SAIDA'
                        THEN quantidade * valor_unitario ELSE 0 END) AS valor_vendas
            FROM app_core.mv_movimentacao
            WHERE data_evento BETWEEN %s AND %s
            GROUP BY DATE_TRUNC('month', data_evento)
            ORDER BY mes
        """, (start, end))

    # =====================================================
    # ESTOQUE TOTAL (TODOS OS PRODUTOS)
    # =====================================================

    def get_total_stock(self):
        result = self.repo.execute_query("""
            SELECT COALESCE(SUM(estoque_atual), 0) AS total
            FROM app_core.vw_product
        """)[0]

        return {"estoque_total": result["total"]}
    
    # =====================================================
    # ESTOQUE POR TIPO
    # (Matéria-prima, Semi-acabado, Acabado)
    # =====================================================

    def get_stock_by_type(self):
        return self.repo.execute_query("""
            SELECT
                tipo,
                SUM(estoque_atual) AS estoque_total
            FROM app_core.vw_product
            GROUP BY tipo
            ORDER BY tipo
        """)


    # =====================================================
    # PRODUTOS CRÍTICOS
    # =====================================================

    '''
    Calculo dos produtos críticos
    '''
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
    # TOP PRODUTOS ACABADOS MAIS VENDIDOS (MÊS ATUAL)
    # =====================================================

    def get_top_selling_products_by_month(
        self,
        year: int,
        month: int,
        limit: int = 5
    ):
        return self.repo.execute_query("""
            SELECT
                m.produto_nome AS nome,
                SUM(m.quantidade) AS total_vendido
            FROM app_core.mv_movimentacao m
            JOIN app_core.vw_product p
                ON p.nome = m.produto_nome
            WHERE m.tipo_movimento = 'SAIDA'
            AND LOWER(p.tipo) = 'produto acabado'
            AND EXTRACT(YEAR FROM m.data_evento) = %s
            AND EXTRACT(MONTH FROM m.data_evento) = %s
            GROUP BY m.produto_nome
            ORDER BY total_vendido DESC
            LIMIT %s
        """, (year, month, limit))


    
    # =====================================================
    # QUANTIDADE DE ITENS VENDIDOS POR MÊS (ANO)
    # =====================================================

    def get_sales_by_month(self, year: int):
        return self.repo.execute_query("""
            SELECT
                DATE_TRUNC('month', data_evento) AS mes,
                SUM(quantidade) AS total_vendido
            FROM app_core.mv_movimentacao
            WHERE tipo_movimento = 'SAIDA'
              AND EXTRACT(YEAR FROM data_evento) = %s
            GROUP BY DATE_TRUNC('month', data_evento)
            ORDER BY mes
        """, (year,))


