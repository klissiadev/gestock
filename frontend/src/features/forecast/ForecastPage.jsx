import { useState, useEffect, useCallback } from "react";
import {
  Box, Typography, Grid, Card, CardContent, Chip, Stack,
  TextField, Button, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, ToggleButtonGroup, ToggleButton,
  CircularProgress, Alert,
} from "@mui/material";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from "recharts";
import { getAnomalies } from "../../api/anomalyAPI.js";
import { ThemeProvider, alpha } from "@mui/material/styles";
import { createTheme } from "@mui/material/styles";


const DAYS     = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
const PIE_COLS = ["#ff3d6e", "#ff7043", "#ffd600", "#ab47bc", "#42a5f5"];

const BarTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <Paper sx={{ p: 1.5, fontSize: 12, border: "1px solid", borderColor: "divider" }}>
      <Typography variant="caption" fontWeight={700} display="block" mb={0.5}>{label}</Typography>
      {payload.map(p => (
        <Typography key={p.name} variant="caption" display="block" sx={{ color: p.fill }}>
          {p.name}: <b>{p.value}</b>
        </Typography>
      ))}
    </Paper>
  );
};

const ForecastPage = () => {
  const today = new Date().toISOString().split("T")[0];
 
  const [dateFilter, setDateFilter]         = useState(today);
  const [data, setData]                     = useState([]);
  const [loading, setLoading]               = useState(false);
  const [error, setError]                   = useState(null);
  const [activeCategory, setActiveCategory] = useState("ALL");
  const getStatus = (d) => Number(d.result ?? d.anomaly);

  const theme = createTheme();

 
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getAnomalies(dateFilter);
      setData(result ?? []);
      setActiveCategory("ALL");
    } catch {
      setError("Falha ao buscar dados da API.");
    } finally {
      setLoading(false);
    }
  }, [dateFilter]);
 
  useEffect(() => {
    fetchData();
  }, [fetchData]);
 
  // ── Dados derivados ──────────────────────────────────────────────────────────
  const categories = ["ALL", ...new Set(data.map(d => d.category))];
  const filtered   = activeCategory === "ALL" ? data : data.filter(d => d.category === activeCategory);
  const anomalies  = filtered.filter(d => Number(getStatus(d)) === -1);
  const normals    = filtered.filter(d => Number(getStatus(d)) === 1);
  const rate       = filtered.length ? ((anomalies.length / filtered.length) * 100).toFixed(1) : "0.0";
 
  const byDay = Array.from({ length: 7 }, (_, i) => ({
    day:       DAYS[i],
    Anomalias: filtered.filter(d => d.day_of_week === i && getStatus(d) === -1).length,
    Normais:   filtered.filter(d => d.day_of_week === i && getStatus(d) ===  1).length,
  }));
 
  const byCat = [...new Set(data.map(d => d.category))].map(cat => ({
    name:  cat,
    value: data.filter(d => d.category === cat && getStatus(d) === -1).length,
  })).filter(c => c.value > 0);
 
  const kpis = [
    { label: "Total Registros", value: filtered.length,  color: "primary.main" },
    { label: "Anomalias",       value: anomalies.length, color: "error.main"   },
    { label: "Normais",         value: normals.length,   color: "success.main" },
    { label: "Taxa Anomalia",   value: `${rate}%`,       color: Number(rate) > 30 ? "error.main" : "primary.main" },
  ];
 
  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ bgcolor: "background.default", minHeight: "100vh", p: 3, color: "text.primary" }}>
 
        {/* ── HEADER ── */}
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3.5}>
          <Box>
            <Typography variant="caption" sx={{ color: "primary.main", letterSpacing: 3, textTransform: "uppercase" }}>
              Sistema de Detecção
            </Typography>
            <Typography variant="h5" fontWeight={800} letterSpacing={-0.5} mt={0.5}>
              Anomaly Dashboard
            </Typography>
          </Box>
 
          <Stack direction="row" spacing={1.5} alignItems="center">
            <TextField
              type="date"
              size="small"
              value={dateFilter}
              onChange={e => setDateFilter(e.target.value)}
              sx={{ "& .MuiOutlinedInput-root": { fontFamily: "inherit", fontSize: 13 } }}
            />
            <Button
              variant="contained"
              onClick={fetchData}
              disabled={loading}
              sx={{
                fontFamily: "inherit", fontWeight: 700, minWidth: 90,
                bgcolor: "primary.main", color: "background.default",
                "&:hover": { bgcolor: "#26d4ec" },
              }}
            >
              {loading
                ? <CircularProgress size={18} thickness={5} sx={{ color: "background.default" }} />
                : "Buscar"}
            </Button>
          </Stack>
        </Stack>
 
        {/* ── ERRO ── */}
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
 
        {/* ── CATEGORY TABS ── */}
        <ToggleButtonGroup
          value={activeCategory}
          exclusive
          onChange={(_, v) => v && setActiveCategory(v)}
          sx={{ flexWrap: "wrap", gap: 1, mb: 3, "& .MuiToggleButtonGroup-grouped": { mr: 0 } }}
        >
          {categories.map(cat => (
            <ToggleButton key={cat} value={cat}>{cat}</ToggleButton>
          ))}
        </ToggleButtonGroup>
 
        {/* ── KPI CARDS ── */}
        <Grid container spacing={2} mb={3}>
          {kpis.map(k => (
            <Grid item xs={12} sm={6} md={3} key={k.label}>
              <Card>
                <CardContent sx={{ pb: "16px !important" }}>
                  <Typography variant="caption" sx={{ color: "text.secondary", textTransform: "uppercase", letterSpacing: 1 }}>
                    {k.label}
                  </Typography>
                  <Typography variant="h4" fontWeight={800} letterSpacing={-1} sx={{ color: k.color, mt: 0.5 }}>
                    {k.value}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
 
        {/* ── GRÁFICOS ── */}
        <Grid container spacing={2} mb={3}>
 
          {/* Bar: anomalias por dia da semana */}
          <Grid item xs={12} md={8}>
            <Card sx={{ p: 2.5 }}>
              <Typography variant="caption" sx={{ color: "text.secondary", textTransform: "uppercase", letterSpacing: 1, display: "block", mb: 2 }}>
                Anomalias por Dia da Semana
              </Typography>
              <ResponsiveContainer width="100%" height={230}>
                <BarChart data={byDay} barCategoryGap="30%" margin={{ top: 5, right: 10, bottom: 0, left: -10 }}>
                  <CartesianGrid stroke="#1e2535" strokeDasharray="3 3" />
                  <XAxis dataKey="day" tick={{ fill: "#7a8299", fontSize: 12, fontFamily: "inherit" }} />
                  <YAxis tick={{ fill: "#7a8299", fontSize: 11, fontFamily: "inherit" }} />
                  <Tooltip content={<BarTooltip />} cursor={{ fill: alpha("#00e5ff", 0.05) }} />
                  <Bar dataKey="Anomalias" fill="#ff3d6e" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="Normais"   fill="#26a269" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Grid>
 
          {/* Pie: anomalias por categoria */}
          <Grid item xs={12} md={4}>
            <Card sx={{ p: 2.5, height: "100%" }}>
              <Typography variant="caption" sx={{ color: "text.secondary", textTransform: "uppercase", letterSpacing: 1, display: "block", mb: 2 }}>
                Anomalias por Categoria
              </Typography>
              {byCat.length === 0 ? (
                <Stack height={230} justifyContent="center" alignItems="center">
                  <Typography variant="caption" color="text.secondary">Sem anomalias no período</Typography>
                </Stack>
              ) : (
                <ResponsiveContainer width="100%" height={230}>
                  <PieChart>
                    <Pie data={byCat} cx="50%" cy="45%" innerRadius={52} outerRadius={80}
                      dataKey="value" nameKey="name" paddingAngle={3}>
                      {byCat.map((_, i) => <Cell key={i} fill={PIE_COLS[i % PIE_COLS.length]} />)}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        background: "#111520", border: "1px solid #1e2535",
                        borderRadius: 8, fontFamily: "inherit", fontSize: 12, color: "#e2e8f0",
                      }}
                    />
                    <Legend iconType="circle" iconSize={8}
                      wrapperStyle={{ fontSize: 11, color: "#7a8299", fontFamily: "inherit" }} />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </Card>
          </Grid>
        </Grid>
 
        {/* ── TABELA ── */}
        <Card sx={{ bgcolor: "card.background" }}>
          <CardContent sx={{ pb: "16px !important" }}>
            <Typography variant="caption" sx={{ color: "text.secondary", textTransform: "uppercase", letterSpacing: 1, display: "block", mb: 2 }}>
              Registros Detalhados
            </Typography>
            <TableContainer component={Paper} sx={{ bgcolor: "transparent" }}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    {["Status", "Item ID", "Nome", "Quantidade", "Preço (R$)", "Tipo", "Loja", "Data de validade"].map(h => (
                      <TableCell key={h} sx={{ color: "text.secondary", fontWeight: 600, fontSize: 11, letterSpacing: 0.5, textTransform: "uppercase", fontFamily: "inherit" }}>
                        {h}
                      </TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filtered.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={8} align="center" sx={{ py: 4, color: "text.secondary", fontFamily: "inherit" }}>
                        {loading ? "Carregando..." : "Nenhum registro encontrado."}
                      </TableCell>
                    </TableRow>
                  ) : filtered.map((row, i) => (
                    <TableRow
                      key={i}
                      sx={{
                        bgcolor: row.result === -1 ? alpha("#ff3d6e", 0.04) : "transparent",
                        "&:hover": { bgcolor: alpha("#00e5ff", 0.04) },
                      }}
                    >
                      <TableCell>
                        <Chip
                          label={row.result === -1 ? "ANOMALIA" : "NORMAL"}
                          size="small"
                          sx={{
                            bgcolor:    row.result === -1 ? alpha("#ff3d6e", 0.15) : alpha("#26a269", 0.15),
                            color:      row.result === -1 ? "#ff3d6e" : "#26a269",
                            fontWeight: 700, fontSize: 10, fontFamily: "inherit", height: 20,
                          }}
                        />
                      </TableCell>
                      <TableCell sx={{ color: "primary.main", fontFamily: "inherit" }}>{row.item_id}</TableCell>
                      <TableCell sx={{ fontFamily: "inherit" }}>{row.nome}</TableCell>
                      <TableCell sx={{ fontFamily: "inherit" }}>{row.quantidade}</TableCell>
                      <TableCell sx={{ fontFamily: "inherit" }}>{Number(row.preco_de_venda)?.toLocaleString("pt-BR")}</TableCell>
                      <TableCell sx={{ color: "text.secondary", fontFamily: "inherit" }}>{row.tipo}</TableCell>
                      <TableCell sx={{ fontFamily: "inherit" }}>{row.cliente}</TableCell>
                      <TableCell sx={{ color: "text.secondary", fontFamily: "inherit" }}>{DAYS[Number(row.data_validade)] ?? "-"}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
 
        <Typography variant="caption" sx={{ display: "block", mt: 2, textAlign: "right", color: "#4a5168" }}>
          Dados via <code>getAnomalies(dataCorte)</code> · anomalyAPI.js
        </Typography>
 
      </Box>
    </ThemeProvider>
  )
}

export default ForecastPage