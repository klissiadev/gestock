import { useState, useEffect, useCallback, useMemo } from "react";
import { Box, Alert, Grid } from "@mui/material";
import { createTheme } from "@mui/material/styles";
import { getAnomalies } from "./services/demandAPI.js";

// Importando nossos novos componentes
import { ForecastHeader } from "./components/ForecastHeader";
import { ForecastFilters } from "./components/ForecastFilters";
import { ForecastKPIs } from "./components/ForecastKPIs";
import { ForecastCharts } from "./components/ForecastCharts";
import { ForecastTable } from "./components/ForecastTable";


const DAYS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

const ForecastPage = () => {
  const yesterday = new Date(Date.now() - 86400000).toISOString().split("T")[0];
  const [dateFilter, setDateFilter] = useState(yesterday);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeCategory, setActiveCategory] = useState("ALL");

  const theme = createTheme();

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getAnomalies(dateFilter);
      setData(result?.data || []);
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

  // ── Lógica de Negócio (Memoizada para performance) ──
  const { categories, filtered, kpis, byDay, byCat } = useMemo(() => {
    // 1. Categorias baseadas nos Clientes do JSON
    const cats = ["ALL", ...new Set(data.map(d => d.cliente))];

    const filteredData = activeCategory === "ALL"
      ? data
      : data.filter(d => d.cliente === activeCategory);

    // 2. Cálculo de KPIs usando o campo 'result' ou 'anomaly'
    const anomalies = filteredData.filter(d => d.result === -1);
    const normals = filteredData.filter(d => d.result === 1);
    const avgScore = anomalies.length
      ? (anomalies.reduce((acc, curr) => acc + Math.abs(curr.score), 0) / anomalies.length).toFixed(3)
      : 0;

    const kpisData = [
      { label: "Total", value: filteredData.length, color: "common.white" },
      { label: "Anomalias", value: anomalies.length, color: "#ff3d6e" },
      { label: "Score Médio", value: avgScore, color: "#ffd600" }, // Novo KPI de intensidade
      { label: "Taxa", value: `${filteredData.length ? ((anomalies.length / filteredData.length) * 100).toFixed(1) : 0}%`, color: "common.white" },
    ];

    // 3. Distribuição por Dia da Semana (extraído de created_at)
    const byDayData = DAYS.map((day, index) => {
      const recordsOnDay = filteredData.filter(d => new Date(d.created_at).getDay() === index);
      return {
        day,
        Anomalias: recordsOnDay.filter(d => d.result === -1).length,
        Normais: recordsOnDay.filter(d => d.result === 1).length,
      };
    });

    // 4. Anomalias por Cliente (para o gráfico de pizza)
    const byCatData = [...new Set(data.map(d => d.cliente))].map(cli => ({
      name: cli,
      value: data.filter(d => d.cliente === cli && d.result === -1).length,
    })).filter(c => c.value > 0);

    return { categories: cats, filtered: filteredData, kpis: kpisData, byDay: byDayData, byCat: byCatData };
  }, [data, activeCategory]);


  return (
    <Box sx={{
      maxHeight: "100vh", p: 3, display: 'grid',
      placeItems: 'center'
    }}>
      <ForecastHeader
        dateFilter={dateFilter}
        setDateFilter={setDateFilter}
        onFetch={fetchData}
        loading={loading}
      />

      <Box sx={{ mt: 3 }}>
        <ForecastFilters
          categories={categories}
          activeCategory={activeCategory}
          setActiveCategory={setActiveCategory}
        />
      </Box>

      {/* ÁREA DOS CARDS - Centralizados no topo */}
      <Grid container spacing={2} justifyContent="center" sx={{ mb: 4 }}>
        <ForecastKPIs kpis={kpis} />
      </Grid>

      {/* ÁREA PRINCIPAL - Lado a lado */}
      <Grid container spacing={3}>
        {error && (
          <Grid item xs={12}>
            <Alert severity="error">{error}</Alert>
          </Grid>
        )}

        {/* COLUNA DA ESQUERDA: Gráficos Empilhados (para dar espaço ao Pizza) */}
        <Grid item xs={12}>
          <ForecastCharts byDay={byDay} byCat={byCat} />
        </Grid>

        {/* COLUNA DA DIREITA: Tabela Detalhada */}
        <Grid item xs={12} lg={7}>
          <ForecastTable filteredData={filtered} loading={loading} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default ForecastPage;