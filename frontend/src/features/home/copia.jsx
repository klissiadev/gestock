import { Box } from "@mui/material";
import CardStock from "./components/CardStock";
import SalesLineChart from "./components/SalesLineChart";
import StockByTypeChart from "./components/StockByTypeChart";
import TopSalesChart from "./components/TopSalesChart";

const STOCK_CARDS = [
  { title: "Estoque total", value: "1.240", percentage: 12, period: "mês" },
  { title: "Matéria Prima", value: "320", percentage: 8, period: "mês" },
  { title: "Semiacabados", value: "210", percentage: 5, period: "mês" },
  { title: "Acabados", value: "110", percentage: 3, period: "mês" },
];


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

export const STOCK_BY_TYPE = [
  { label: "Matéria Prima", value: 260 },
  { label: "Semiacabado", value: 450 },
  { label: "Acabado", value: 140 },
];

export const TOP_SALES = [
  { product: "Headset Gamer", total: 650 },
  { product: "Mouse Gamer RGB", total: 580 },
  { product: "Mouse Óptico", total: 540 },
  { product: "Teclado Gamer", total: 520 },
  { product: "Teclado Mecânico RGB", total: 460 },
];

export default function HomePage2() {
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
          <TopSalesChart topSales={TOP_SALES} period={"Dezembro"} />
        </Box>
        
      </Box>
    </Box>
  );
}
