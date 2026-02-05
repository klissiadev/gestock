from fastapi import APIRouter, Depends, Query
from datetime import date

from backend.database.base import get_connection
from backend.database.repository import Repository
from backend.services.analytics_view import AnalyticsService

router = APIRouter(tags=["Analytics"])


# =====================================================
# DEPENDENCIES
# =====================================================

def get_repository():
    conn = get_connection()
    try:
        yield Repository(conn)
    finally:
        conn.close()


def get_analytics_service(
    repo: Repository = Depends(get_repository)
):
    return AnalyticsService(repo)


# =====================================================
# KPIs GERAIS DE ESTOQUE
# =====================================================

@router.get("/stock-kpis")
def stock_kpis(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_stock_kpis()


# =====================================================
# ESTOQUE POR TIPO
# =====================================================

@router.get("/stock-by-type")
def stock_by_type(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_stock_by_type()


# =====================================================
# PRODUTOS CRÍTICOS
# =====================================================

@router.get("/critical-products")
def critical_products(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_critical_products()


# =====================================================
# MOVIMENTAÇÃO POR PERÍODO
# =====================================================

@router.get("/movimentacao-periodo")
def movimentacao_periodo(
    start: date = Query(..., description="YYYY-MM-DD"),
    end: date = Query(..., description="YYYY-MM-DD"),
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_movimentacao_por_periodo(start, end)


# =====================================================
# KPIs FINANCEIROS
# =====================================================

@router.get("/financial-kpis")
def financial_kpis(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_financial_kpis()


# =====================================================
# PRODUTOS MAIS VENDIDOS
# =====================================================

@router.get("/top-selling")
def top_selling(
    limit: int = Query(5, ge=1, le=50),
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_top_selling_products(limit)


# =====================================================
# PRODUTOS PRÓXIMOS DO VENCIMENTO
# =====================================================

@router.get("/near-expiration")
def near_expiration(
    days: int = Query(30, ge=1, le=365),
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_products_near_expiration(days)


# =====================================================
# PRODUÇÃO / CONSUMO
# =====================================================

@router.get("/production-summary")
def production_summary(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_production_summary()


# =====================================================
# GIRO DE ESTOQUE
# =====================================================

@router.get("/stock-turnover")
def stock_turnover(
    start: date = Query(...),
    end: date = Query(...),
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_stock_turnover(start, end)
