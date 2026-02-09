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
} from "@mui/material";
import { useEffect, useState } from "react";
import { BarChart, PieChart } from "@mui/x-charts";

import {
  getStockKpis,
  getStockByType,
  getCriticalProducts,
  getTopSelling,
  getFinancialKpis,
} from "../../api/analyticsApi";

function KpiCard({ title, value }) {
  return (
    <Paper sx={{ p: 2, textAlign: "center" }}>
      <Typography variant="body2" color="text.secondary">
        {title}
      </Typography>
      <Typography variant="h4" sx={{ mt: 1 }}>
        {value}
      </Typography>
    </Paper>
  );
}

export default function HomePage() {
  const [stockKpis, setStockKpis] = useState(null);
  const [stockByType, setStockByType] = useState([]);
  const [criticalProducts, setCriticalProducts] = useState([]);
  const [topSelling, setTopSelling] = useState([]);
  const [financialKpis, setFinancialKpis] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      getStockKpis(),
      getStockByType(),
      getCriticalProducts(),
      getTopSelling(),
      getFinancialKpis(),
    ])
      .then(
        ([
          stockKpisRes,
          stockByTypeRes,
          criticalProductsRes,
          topSellingRes,
          financialKpisRes,
        ]) => {
          setStockKpis(stockKpisRes);
          setStockByType(stockByTypeRes);
          setCriticalProducts(criticalProductsRes);
          setTopSelling(topSellingRes);
          setFinancialKpis(financialKpisRes);
        }
      )
      .catch(() => setError("Erro ao carregar dashboard"));
  }, []);

  if (error) return <Typography color="error">{error}</Typography>;
  if (!stockKpis || !financialKpis) return <Typography>Carregando…</Typography>;

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: "auto" }}>
      <Typography variant="h4" gutterBottom align="center">
        Dashboard
      </Typography>

      {/* KPIs */}
      <Grid container spacing={3} sx={{ mb: 5 }}>
        <Grid item xs={12} md={4}>
          <KpiCard title="Estoque Total" value={stockKpis.estoque_total} />
        </Grid>
        <Grid item xs={12} md={4}>
          <KpiCard
            title="Produtos em Baixo Estoque"
            value={stockKpis.produtos_baixo_estoque}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <KpiCard
            title="Produtos Vencidos"
            value={stockKpis.produtos_vencidos}
          />
        </Grid>
      </Grid>

      {/* Gráficos */}
      <Grid container spacing={4} sx={{ mb: 5 }}>
        {/* Estoque por tipo */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" align="center">
              Estoque por Tipo
            </Typography>
            <Divider sx={{ my: 2 }} />
            <BarChart
              height={300}
              xAxis={[
                {
                  scaleType: "band",
                  data: stockByType.map((i) => i.tipo),
                },
              ]}
              series={[
                {
                  data: stockByType.map((i) => i.estoque_total),
                  label: "Estoque",
                },
              ]}
            />
          </Paper>
        </Grid>

        {/* Financeiro */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" align="center">
              Financeiro
            </Typography>
            <Divider sx={{ my: 2 }} />
            <PieChart
              height={300}
              series={[
                {
                  data: [
                    {
                      id: 0,
                      value: financialKpis.valor_compras,
                      label: "Compras",
                    },
                    {
                      id: 1,
                      value: financialKpis.valor_vendas,
                      label: "Vendas",
                    },
                    {
                      id: 2,
                      value: financialKpis.margem_bruta_estimada,
                      label: "Margem",
                    },
                  ],
                },
              ]}
            />
          </Paper>
        </Grid>
      </Grid>

      {/* Produtos críticos */}
      <Paper sx={{ p: 3, mb: 5 }}>
        <Typography variant="h6" align="center">
          Produtos Críticos
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Produto</TableCell>
              <TableCell align="right">Estoque</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {criticalProducts.map((p) => (
              <TableRow key={p.id}>
                <TableCell>{p.nome}</TableCell>
                <TableCell align="right">
                  {p.estoque_atual}/{p.estoque_minimo}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>

      {/* Top vendidos */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" align="center">
          Top Vendidos
        </Typography>
        <Divider sx={{ my: 2 }} />
        <BarChart
          height={320}
          xAxis={[
            {
              scaleType: "band",
              data: topSelling.map((p) => p.nome),
            },
          ]}
          series={[
            {
              data: topSelling.map((p) => p.total_vendido),
              label: "Quantidade vendida",
            },
          ]}
        />
      </Paper>
    </Box>
  );
}
