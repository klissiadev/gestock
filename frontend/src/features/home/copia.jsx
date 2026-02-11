import { Box } from "@mui/material";
import CardStock from "./components/CardStock";
import SalesLineChart from "./components/SalesLineChart";

const STOCK_CARDS = [
  { title: "Produtos em estoque", value: "1.240", percentage: 12, period: "mês" },
  { title: "Movimentações", value: "320", percentage: 8, period: "mês" },
  { title: "Entradas", value: "210", percentage: 5, period: "mês" },
  { title: "Saídas", value: "110", percentage: 3, period: "mês" },
];

// mockChartData.js
export const SALES_BY_MONTH = [
  { month: "Jan", value: 100 },
  { month: "Fev", value: 35 },
  { month: "Mar", value: 130 },
  { month: "Abr", value: 300 },
  { month: "Mai", value: 285 },
  { month: "Jun", value: 240 },
  { month: "Jul", value: 275 },
  { month: "Ago", value: 275 },
  { month: "Set", value: 310 },
  { month: "Out", value: 90 },
  { month: "Nov", value: 220 },
  { month: "Dez", value: 280 },
];

export default function HomePage() {
  return (
    <Box sx={{ width: "100%", p: 1 }}>
      <Box
        sx={{
          width: "100%",
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: 2,
        }}
      >
        <Box
          sx={{
            width: "100%",
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: 2,
          }}
        >
          {STOCK_CARDS.map((card, index) => (
            <CardStock key={index} {...card} />
          ))}
        </Box>
        <Box sx={{ mt: 2 }}>
          <SalesLineChart salesByMonth={SALES_BY_MONTH} />
        </Box>
      </Box>
    </Box>
  );
}
