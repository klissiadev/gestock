import { BarChart } from "@mui/x-charts/BarChart";
import { useTheme } from "@mui/material/styles";

export default function FinancialBarChart({ data }) {

  const theme = useTheme();

  return (
    <BarChart
      xAxis={[
        {
          scaleType: "band",
          data: data.map((d) => d.month),
        },
      ]}
      series={[
        {
          data: data.map((d) => d.compras),
          label: "Compras",
          color: theme.palette.uploadBox.button,
        },
        {
          data: data.map((d) => d.vendas),
          label: "Vendas",
          color: theme.palette.iconButton.active,
        },
      ]}
      height={180}
    />
  );
}