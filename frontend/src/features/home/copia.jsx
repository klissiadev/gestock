// frontend/src/features/home/HomePage.jsx
import { Box } from "@mui/material";
import { useEffect, useState } from "react";

import CardStock from "./components/CardStock";
import SalesLineChart from "./components/SalesLineChart";
import TopSalesChart from "./components/TopSalesChart";
import CriticalItemsCard from "./components/CriticalItensCard";
import FinancialBarChart from "./components/FinancialBarChart"; 

import { useHeader } from "../../HeaderContext";

import {
  getTotalStock,
  getStockByType,
  getCriticalProducts,
  getSalesByMonth,
  getTopSellingProductsByMonth,
  getFinancialKpisByYear, 
} from "../../api/analyticsApi";

function formatMonthFromDate(dateString) {
  const date = new Date(dateString);

  const months = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
  ];

  return months[date.getMonth()];
}

function getMonthName(monthNumber) {
  const months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
  ];

  return months[monthNumber - 1] ?? "";
}

export default function HomePage() {
  const [STOCK_CARDS, setStockCards] = useState([]);
  const [SALES_BY_MONTH, setSalesByMonth] = useState([]);
  const [TOP_SALES, setTopSales] = useState([]);
  const [EXPIRING_ITEMS, setExpiringItems] = useState([]);
  const [FINANCIAL_DATA, setFinancialData] = useState([]);

  const { setHeaderConfig } = useHeader();

  const [year, setYear] = useState(2026);
  const [month, setMonth] = useState(5);

  // =============================
  // HEADER CONFIG
  // =============================
  useEffect(() => {
    setHeaderConfig({
      variant: "home",
      period: { year, month },
      onPeriodChange: ({ year: newYear, month: newMonth }) => {
        setYear(newYear);
        setMonth(newMonth);
      },
    });

    return () => {
      setHeaderConfig({});
    };
  }, [year, month]);

  // =============================
  // LOAD DASHBOARD DATA
  // =============================
  useEffect(() => {
    async function loadData() {
      try {
        const [
          totalStockRes,
          stockByTypeRes,
          criticalProductsRes,
          salesByMonthRes,
          topSellingRes,
          financialRes, // 👈 NOVO
        ] = await Promise.all([
          getTotalStock(),
          getStockByType(),
          getCriticalProducts(),
          getSalesByMonth(year),
          getTopSellingProductsByMonth(year, month),
          getFinancialKpisByYear(year), // 👈 NOVO
        ]);

        // =============================
        // CARDS DE ESTOQUE
        // =============================
        const cards = [
          {
            title: "Estoque total",
            value: totalStockRes.estoque_total ?? 0,
            percentage: 0,
            period: "ano",
          },
          ...stockByTypeRes.map((item) => ({
            title: item.tipo,
            value: item.estoque_total ?? 0,
            percentage: 0,
            period: "ano",
          })),
        ];

        setStockCards(cards);

        // =============================
        // VENDAS (QUANTIDADE)
        // =============================
        const salesFormatted = salesByMonthRes.map((m) => ({
          month: formatMonthFromDate(m.mes),
          value: m.total_vendido,
        }));

        setSalesByMonth(salesFormatted);

        // =============================
        // FINANCEIRO (COMPRAS x VENDAS)
        // =============================
        const financialFormatted = financialRes.map((m) => ({
          month: formatMonthFromDate(m.mes),
          compras: m.valor_compras ?? 0,
          vendas: m.valor_vendas ?? 0,
        }));

        setFinancialData(financialFormatted);

        // =============================
        // TOP VENDAS
        // =============================
        const topFormatted = topSellingRes.map((p) => ({
          product: p.nome,
          total: p.total_vendido,
        }));

        setTopSales(topFormatted);

        // =============================
        // PRODUTOS CRÍTICOS
        // =============================
        const criticalFormatted = criticalProductsRes.map((p) => ({
          product: p.nome,
          quantity: p.estoque_atual,
          due: p.data_validade,
          status: "Crítico",
        }));

        setExpiringItems(criticalFormatted);

      } catch (error) {
        console.error("Erro ao carregar dashboard:", error);
      }
    }

    loadData();
  }, [year, month]);

  return (
    <Box
      sx={{
        width: "100%",
        p: 1,
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      {/* ================================= */}
      {/* BLOCO SUPERIOR */}
      {/* ================================= */}
      <Box sx={{ display: "flex", gap: 2 }}>
        <Box
          sx={{
            width: "45%",
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: 2,
          }}
        >
          {STOCK_CARDS.map((card, index) => (
            <CardStock key={index} {...card} />
          ))}
        </Box>

        <Box sx={{ width: "55%" }}>
          <SalesLineChart salesByMonth={SALES_BY_MONTH} />
        </Box>
      </Box>

      {/* ================================= */}
      {/* FINANCEIRO */}
      {/* ================================= */}
      <Box sx={{ width: "100%" }}>
        <FinancialBarChart data={FINANCIAL_DATA} />
      </Box>

      {/* ================================= */}
      {/* BLOCO INFERIOR */}
      {/* ================================= */}
      <Box sx={{ display: "flex", gap: 2 }}>
        <Box width="45%">
          <CriticalItemsCard criticalItems={EXPIRING_ITEMS} />
        </Box>

        <Box width="55%">
          <TopSalesChart
            topSales={TOP_SALES}
            period={getMonthName(month)}
          />
        </Box>
      </Box>
    </Box>
  );
}