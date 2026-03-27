import { useState, useEffect, useCallback, useMemo } from "react";
import { Box, Alert, Typography } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { getAnomalies } from "./services/demandAPI.js";

// Importando nossos novos componentes
import { ForecastHeader } from "./components/ForecastHeader";
import { ForecastFilters } from "./components/ForecastFilters";
import { ForecastKPIs } from "./components/ForecastKPIs";
import { ForecastCharts } from "./components/ForecastCharts";
import { ForecastTable } from "./components/ForecastTable";


const DAYS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

const ForecastPage = () => {
  const today = new Date().toISOString().split("T")[0];

  const [dateFilter, setDateFilter] = useState(today);
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
    const getStatus = (d) => Number(d.result ?? d.anomaly);
    const cats = ["ALL", ...new Set(data.map(d => d.category))];
    const filteredData = activeCategory === "ALL" ? data : data.filter(d => d.category === activeCategory);

    const anomalies = filteredData.filter(d => getStatus(d) === -1);
    const normals = filteredData.filter(d => getStatus(d) === 1);
    const rate = filteredData.length ? ((anomalies.length / filteredData.length) * 100).toFixed(1) : "0.0";

    const kpisData = [
      { label: "Total Registros", value: filteredData.length, color: "common.white" },
      { label: "Anomalias", value: anomalies.length, color: "error.main" },
      { label: "Normais", value: normals.length, color: "success.main" },
      { label: "Taxa Anomalia", value: `${rate}%`, color: Number(rate) > 30 ? "error.main" : "common.white" },
    ];

    const byDayData = Array.from({ length: 7 }, (_, i) => ({
      day: DAYS[i],
      Anomalias: filteredData.filter(d => d.day_of_week === i && getStatus(d) === -1).length,
      Normais: filteredData.filter(d => d.day_of_week === i && getStatus(d) === 1).length,
    }));

    const byCatData = [...new Set(data.map(d => d.category))].map(cat => ({
      name: cat,
      value: data.filter(d => d.category === cat && getStatus(d) === -1).length,
    })).filter(c => c.value > 0);

    return { categories: cats, filtered: filteredData, kpis: kpisData, byDay: byDayData, byCat: byCatData };
  }, [data, activeCategory]);

  return (
    <Box sx={{ minHeight: "100vh", p: 2, color: "text.primary" }}>

        <ForecastHeader
          dateFilter={dateFilter}
          setDateFilter={setDateFilter}
          onFetch={fetchData}
          loading={loading}
        />
        <ForecastFilters
          categories={categories}
          activeCategory={activeCategory}
          setActiveCategory={setActiveCategory}
        />
        <Box sx={{ display:"flex"}}>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          <Box sx={{display:"flex", flexDirection:"column", width:"55%"}}>
            
            <ForecastKPIs kpis={kpis} />

            <ForecastCharts byDay={byDay} byCat={byCat} />
          </Box>
          <Box sx={{display:"flex", flexDirection:"column", width:"45%"}}>
            <ForecastTable filteredData={filtered} loading={loading} />

          </Box>
      </Box>

      <Typography variant="caption" sx={{ display: "block", mt: 2, textAlign: "right", color: "#4a5168" }}>
        Dados via <code>getAnomalies(dataCorte)</code> · anomalyAPI.js
      </Typography>

      </Box>
  );
};

export default ForecastPage;