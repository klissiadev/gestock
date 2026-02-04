from fastapi import APIRouter, Depends, Query
from datetime import date
from backend.database.base import get_connection
from backend.database.repository import Repository
from backend.services.analytics_view import AnalyticsService

router = APIRouter()

# =====================================================
# KPIs GERAIS DE ESTOQUE
# =====================================================

@router.get("/stock-kpis")
def get_stock_kpis(repo: Repository = Depends(get_connection)):
    service = AnalyticsService(repo)
    return service.get_stock_kpis()


# =====================================================
# ESTOQUE POR TIPO
# =====================================================

@router.get("/stock-by-type")
def get_stock_by_type(repo: Repository = Depends(get_connection)):
    service = AnalyticsService(repo)
    return service.get_stock_by_type()


# =====================================================
# PRODUTOS CRÍTICOS
# =====================================================

@router.get("/critical-products")
def get_critical_products(repo: Repository = Depends(get_connection)):
    service = AnalyticsService(repo)
    return service.get_critical_products()


# =====================================================
# MOVIMENTAÇÃO POR PERÍODO
# =====================================================

@router.get("/movimentacao-periodo")
def get_movimentacao_por_periodo(
    start: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end: date = Query(..., description="Data final (YYYY-MM-DD)"),
    repo: Repository = Depends(get_connection)
):
    service = AnalyticsService(repo)
    return service.get_movimentacao_por_periodo(start, end)


# =====================================================
# KPIs FINANCEIROS
# =====================================================

@router.get("/financial-kpis")
def get_financial_kpis(repo: Repository = Depends(get_connection)):
    service = AnalyticsService(repo)
    return service.get_financial_kpis()


# =====================================================
# PRODUTOS MAIS VENDIDOS
# =====================================================

@router.get("/top-selling")
def get_top_selling_products(
    limit: int = Query(5, ge=1, le=50),
    repo: Repository = Depends(get_connection)
):
    service = AnalyticsService(repo)
    return service.get_top_selling_products(limit)


# =====================================================
# PRODUTOS PRÓXIMOS DO VENCIMENTO
# =====================================================

@router.get("/near-expiration")
def get_products_near_expiration(
    days: int = Query(30, ge=1, le=365),
    repo: Repository = Depends(get_connection)
):
    service = AnalyticsService(repo)
    return service.get_products_near_expiration(days)


# =====================================================
# PRODUÇÃO / CONSUMO
# =====================================================

@router.get("/production-summary")
def get_production_summary(repo: Repository = Depends(get_connection)):
    service = AnalyticsService(repo)
    return service.get_production_summary()


# =====================================================
# GIRO DE ESTOQUE
# =====================================================

@router.get("/stock-turnover")
def get_stock_turnover(
    start: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end: date = Query(..., description="Data final (YYYY-MM-DD)"),
    repo: Repository = Depends(get_connection)
):
    service = AnalyticsService(repo)
    return service.get_stock_turnover(start, end)
