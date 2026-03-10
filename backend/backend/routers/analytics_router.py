from fastapi import APIRouter, Depends, Query
from datetime import date
from backend.database.base import get_connection
from backend.database.repository import Repository
from backend.services.analytics_view import AnalyticsService

router = APIRouter()

# =========================
# DEPENDENCIES
# =========================

def get_repository():
    conn = get_connection()
    try:
        yield Repository(conn)
    finally:
        conn.close()

def get_service(repo: Repository = Depends(get_repository)):
    return AnalyticsService(repo)


# =====================================================
# ESTOQUE TOTAL
# =====================================================

@router.get("/total-stock")
def total_stock(service: AnalyticsService = Depends(get_service)):
    return service.get_total_stock()


# =====================================================
# ESTOQUE POR TIPO
# =====================================================

@router.get("/stock-by-type")
def stock_by_type(service: AnalyticsService = Depends(get_service)):
    return service.get_stock_by_type()


# =====================================================
# PRODUTOS CRÍTICOS
# =====================================================

@router.get("/critical-products")
def critical_products(service: AnalyticsService = Depends(get_service)):
    return service.get_critical_products()


# =====================================================
# VENDAS POR MÊS (ANO)
# =====================================================

@router.get("/sales-by-month")
def sales_by_month(
    year: int = Query(...),
    service: AnalyticsService = Depends(get_service)
):
    return service.get_sales_by_month(year)


# =====================================================
# TOP PRODUTOS POR MÊS
# =====================================================

@router.get("/top-selling-products")
def top_selling_products(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    limit: int = Query(5, ge=1, le=50),
    service: AnalyticsService = Depends(get_service)
):
    return service.get_top_selling_products_by_month(year, month, limit)

# =====================================================
# KPIs FINANCEIROS POR PERÍODO
# =====================================================

@router.get("/financial-kpis-by-year")
def financial_kpis_by_year(
    year: int = Query(...),
    service: AnalyticsService = Depends(get_service)
):
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    return service.get_financial_kpis_por_mes(start, end)