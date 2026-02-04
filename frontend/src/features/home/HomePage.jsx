import { Box } from "@mui/material";
import { useEffect, useState } from "react";
import { getStockKpis } from "../../api/analyticsApi";

export default function HomePage() {
  const [kpis, setKpis] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getStockKpis()
      .then(setKpis)
      .catch((err) => {
        console.error(err);
        setError("Erro ao buscar KPIs");
      });
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <h1>Dashboard (teste)</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!kpis && !error && <p>Carregando...</p>}

      {kpis && (
        <pre style={{ background: "#f4f4f4", padding: "16px" }}>
          {JSON.stringify(kpis, null, 2)}
        </pre>
      )}
    </Box>
  );
}
