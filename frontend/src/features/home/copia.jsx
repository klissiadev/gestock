import { Box } from "@mui/material";
import { useEffect, useState } from "react";

import CardStock from "./components/CardStock";
import SalesLineChart from "./components/SalesLineChart";
import StockByTypeChart from "./components/StockByTypeChart";
import TopSalesChart from "./components/TopSalesChart";
import ExpiringItemsCard from "./components/ExpiredItensCard";

import {
  getTotalStock,
  getStockByType,
  getCriticalProducts,
  getSalesByMonth,
  getTopSellingProductsByMonth,
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


export default function HomePage2() {
  const [STOCK_CARDS, setStockCards] = useState([]);
  const [SALES_BY_MONTH, setSalesByMonth] = useState([]);
  const [STOCK_BY_TYPE, setStockByType] = useState([]);
  const [TOP_SALES, setTopSales] = useState([]);
  const [EXPIRING_ITEMS, setExpiringItems] = useState([]);

  const year = 2026;
  const month = 5;

  useEffect(() => {
    async function loadData() {
      try {
        const [
          totalStockRes,
          stockByTypeRes,
          criticalProductsRes,
          salesByMonthRes,
          topSellingRes,
        ] = await Promise.all([
          getTotalStock(),
          getStockByType(),
          getCriticalProducts(),
          getSalesByMonth(year),
          getTopSellingProductsByMonth(year, month),
        ]);

        console.log("totalStockRes", totalStockRes);
        console.log("stockByTypeRes", stockByTypeRes);
        console.log("salesByMonthRes", salesByMonthRes);
        console.log("topSellingRes", topSellingRes);
        console.log("criticalProductsRes", criticalProductsRes);

        // CARDS
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

        // VENDAS POR MÊS
        const salesFormatted = salesByMonthRes.map((m) => ({
          month: formatMonthFromDate(m.mes),
          value: m.total_vendido,
        }));

        setSalesByMonth(salesFormatted);

        // ESTOQUE POR TIPO (baixo estoque)
        const stockFormatted = stockByTypeRes.map((item) => ({
          label: item.tipo,
          value: item.estoque_total ?? 0,
        }));

        setStockByType(stockFormatted);

        // TOP VENDAS
        const topFormatted = topSellingRes.map((p) => ({
          product: p.nome,
          total: p.total_vendido,
        }));

        setTopSales(topFormatted);

        // PRODUTOS CRÍTICOS
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
  }, []);

  return (
    <Box sx={{ width: "100%", p: 1 , display: "flex", flexDirection:"column", gap: 2,}}>
      <Box
        sx={{
          display:"flex",
          flexDirection:"row",
          gap: 2,
        }}
      >
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
        <Box sx={{ mt: 2, width:"55%"}}>
          <SalesLineChart salesByMonth={SALES_BY_MONTH} />
        </Box>
      </Box>
      <Box
        sx={{
          display:"flex",
          flexDirection:"row",
          gap: 2,
        }}
      >
        <Box width={"30%"}>
          <StockByTypeChart stockByType={STOCK_BY_TYPE} period={"Dezembro"}/>
        </Box>
        <Box width={"35%"}>
          <TopSalesChart topSales={TOP_SALES} period={getMonthName(month)}/>
        </Box>
        <Box width={"35%"}>
          <ExpiringItemsCard expiringItems={EXPIRING_ITEMS}/>
        </Box>
      </Box>
    </Box>
  );
}
