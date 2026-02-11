import {
  Box,
  Grid,
  Paper,
  Typography,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Select,
  MenuItem,
} from "@mui/material";
import { BarChart, LineChart } from "@mui/x-charts";
import { useEffect, useState } from "react";

import {
  getTotalStock,
  getStockByType,
  getCriticalProducts,
  getSalesByMonth,
  getTopSellingProductsByMonth,
} from "../../api/analyticsApi";

const months = [
  "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
  "Jul", "Ago", "Set", "Out", "Nov", "Dez",
];

export default function Home() {
  const currentYear = new Date().getFullYear();

  const [year, setYear] = useState(currentYear);
  const [month, setMonth] = useState(new Date().getMonth() + 1);

  const [totalStock, setTotalStock] = useState(0);
  const [stockByType, setStockByType] = useState([]);
  const [criticalProducts, setCriticalProducts] = useState([]);
  const [salesByMonth, setSalesByMonth] = useState([]);
  const [topProducts, setTopProducts] = useState([]);


  useEffect(() => {
    console.log("SalesByMonth atualizado:", salesByMonth);
  }, [salesByMonth]);

  // ===============================
  // LOAD FIXED DATA
  // ===============================
  useEffect(() => {
    getTotalStock().then((res) => setTotalStock(res.estoque_total));
    getStockByType().then(setStockByType);
    getCriticalProducts().then(setCriticalProducts);
  }, []);

  // ===============================
  // LOAD YEAR DATA
  // ===============================
  useEffect(() => {
    getSalesByMonth(year).then(setSalesByMonth);
  }, [year]);

  // ===============================
  // LOAD MONTH DATA
  // ===============================
  useEffect(() => {
    getTopSellingProductsByMonth(year, month).then(setTopProducts);
  }, [year, month]);

  const stockMap = Object.fromEntries(
    stockByType.map((item) => [item.tipo, item.estoque_total])
  );

  const salesMap = Object.fromEntries(
    salesByMonth.map((item) => [
      new Date(item.mes).getMonth(),
      Number(item.total_vendido),
    ])
  );

  const fullYearData = months.map((_, index) => salesMap[index] || 0);

  console.log("RENDER HOME");

  console.log("salesByMonth RAW:", salesByMonth);
  console.log("salesMap:", salesMap);
  console.log("fullYearData:", fullYearData);
  console.log("months:", months);


  return (
    <Box p={3}>
      <Typography variant="h5" gutterBottom>
        Dashboard de Estoque e Vendas
      </Typography>

      {/* =======================
          KPIs
      ======================= */}
      <Grid container spacing={2}>
        {[
          { label: "Estoque Total", value: totalStock },
          { label: "Matéria-Prima", value: stockMap["MATERIA_PRIMA"] || 0 },
          { label: "Semiacabados", value: stockMap["SEMI_ACABADO"] || 0 },
          { label: "Acabados", value: stockMap["ACABADO"] || 0 },
        ].map((item) => (
          <Grid item xs={12} md={3} key={item.label}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle2">{item.label}</Typography>
              <Typography variant="h6">{item.value}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* =======================
          ESTOQUE POR TIPO
      ======================= */}
      <Paper sx={{ p: 2, mt: 3 }}>
        <Typography variant="subtitle1">Estoque por Tipo</Typography>
        <BarChart
          height={300}
          xAxis={[{ data: stockByType.map((s) => s.tipo), scaleType: "band" }]}
          series={[{ data: stockByType.map((s) => s.estoque_total) }]}
        />
      </Paper>

      {/* =======================
          FILTROS
      ======================= */}
      <Box mt={3} display="flex" gap={2}>
        <Select value={year} onChange={(e) => setYear(e.target.value)}>
          {[2024, 2025, 2026, 2027].map((y) => (
            <MenuItem key={y} value={y}>{y}</MenuItem>
          ))}
        </Select>

        <Select value={month} onChange={(e) => setMonth(e.target.value)}>
          {months.map((m, i) => (
            <MenuItem key={i} value={i + 1}>{m}</MenuItem>
          ))}
        </Select>
      </Box>

      {/* =======================
          VENDAS POR MÊS
      ======================= */}
      <Paper sx={{ p: 2, mt: 3 }}>
        <Typography variant="subtitle1">
          Quantidade Vendida por Mês ({year})
        </Typography>
        <LineChart
          width={900}
          height={300}
          xAxis={[
            {
              data: months,
              scaleType: "point",
            },
          ]}
          yAxis={[
            {
              min: 0,
            },
          ]}
          series={[
            {
              id: "vendas",
              data: fullYearData.map((n) => Number(n) || 0),
            },
          ]}
        />


      </Paper>

      {/* =======================
          TOP PRODUTOS
      ======================= */}
      <Paper sx={{ p: 2, mt: 3 }}>
        <Typography variant="subtitle1">
          Top Produtos Acabados – {months[month - 1]}/{year}
        </Typography>
        {topProducts.map((p) => (
          <Typography key={p.nome}>
            {p.nome} — {p.total_vendido}
          </Typography>
        ))}
      </Paper>
    

      {/* =======================
          PRODUTOS CRÍTICOS
      ======================= */}
      <Paper sx={{ p: 2, mt: 3 }}>
        <Typography variant="subtitle1">Itens Críticos</Typography>
        <Divider sx={{ my: 1 }} />
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Produto</TableCell>
              <TableCell>Estoque Atual</TableCell>
              <TableCell>Estoque Mínimo</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {criticalProducts.map((p) => (
              <TableRow key={p.id}>
                <TableCell>{p.nome}</TableCell>
                <TableCell>{p.estoque_atual}</TableCell>
                <TableCell>{p.estoque_minimo}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
}
