const BASE_URL = "http://localhost:8000/analytics";

// ===============================
// KPIs GERAIS
// ===============================
export async function getStockKpis() {
  const res = await fetch(`${BASE_URL}/stock-kpis`);
  if (!res.ok) throw new Error("Erro ao buscar KPIs");
  return res.json();
}

// ===============================
// ESTOQUE POR TIPO
// ===============================
export async function getStockByType() {
  const res = await fetch(`${BASE_URL}/stock-by-type`);
  if (!res.ok) throw new Error("Erro ao buscar estoque por tipo");
  return res.json();
}

// ===============================
// PRODUTOS CRÍTICOS
// ===============================
export async function getCriticalProducts() {
  const res = await fetch(`${BASE_URL}/critical-products`);
  if (!res.ok) throw new Error("Erro ao buscar produtos críticos");
  return res.json();
}

// ===============================
// TOP VENDIDOS
// ===============================
export async function getTopSelling(limit = 5) {
  const res = await fetch(`${BASE_URL}/top-selling?limit=${limit}`);
  if (!res.ok) throw new Error("Erro ao buscar top vendidos");
  return res.json();
}

// ===============================
// FINANCEIRO
// ===============================
export async function getFinancialKpis() {
  const res = await fetch(`${BASE_URL}/financial-kpis`);
  if (!res.ok) throw new Error("Erro ao buscar KPIs financeiros");
  return res.json();
}

// ===============================
// MOVIMENTAÇÃO POR PERÍODO
// ===============================
export async function getMovimentacaoPeriodo(start, end) {
  const res = await fetch(
    `${BASE_URL}/movimentacao-periodo?start=${start}&end=${end}`
  );
  if (!res.ok) throw new Error("Erro ao buscar movimentação");
  return res.json();
}

// ===============================
// GIRO DE ESTOQUE
// ===============================
export async function getStockTurnover(start, end) {
  const res = await fetch(
    `${BASE_URL}/stock-turnover?start=${start}&end=${end}`
  );
  if (!res.ok) throw new Error("Erro ao buscar giro de estoque");
  return res.json();
}
