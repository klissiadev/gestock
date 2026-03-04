const BASE_URL = "http://localhost:8000/analytics";

// =====================================================
// ESTOQUE TOTAL (TODOS OS PRODUTOS)
// =====================================================
export async function getTotalStock() {
  const res = await fetch(`${BASE_URL}/total-stock`);
  if (!res.ok) throw new Error("Erro ao buscar estoque total");
  return res.json();
}

// =====================================================
// ESTOQUE POR TIPO
// =====================================================
export async function getStockByType() {
  const res = await fetch(`${BASE_URL}/stock-by-type`);
  if (!res.ok) throw new Error("Erro ao buscar estoque por tipo");
  return res.json();
}

// =====================================================
// PRODUTOS CRÍTICOS
// =====================================================
export async function getCriticalProducts() {
  const res = await fetch(`${BASE_URL}/critical-products`);
  if (!res.ok) throw new Error("Erro ao buscar produtos críticos");
  return res.json();
}

// =====================================================
// QUANTIDADE DE ITENS VENDIDOS POR MÊS (ANO)
// =====================================================
export async function getSalesByMonth(year) {
  const res = await fetch(
    `${BASE_URL}/sales-by-month?year=${year}`
  );
  if (!res.ok) throw new Error("Erro ao buscar vendas por mês");
  return res.json();
}

// =====================================================
// TOP PRODUTOS ACABADOS MAIS VENDIDOS (ANO + MÊS)
// =====================================================
export async function getTopSellingProductsByMonth(
  year,
  month,
  limit = 5
) {
  const res = await fetch(
    `${BASE_URL}/top-selling-products?year=${year}&month=${month}&limit=${limit}`
  );
  if (!res.ok) throw new Error("Erro ao buscar top produtos vendidos");
  return res.json();
}


// =====================================================
// KPIs FINANCEIROS (COMPRAS x VENDAS POR ANO)
// =====================================================
export async function getFinancialKpisByYear(year) {
  const res = await fetch(
    `${BASE_URL}/financial-kpis-by-year?year=${year}`
  );
  if (!res.ok) throw new Error("Erro ao buscar KPIs financeiros");
  return res.json();
}