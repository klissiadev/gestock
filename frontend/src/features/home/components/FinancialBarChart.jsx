import { BarChart } from "@mui/x-charts/BarChart";

export default function FinancialBarChart({ data }) {
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
        },
        {
          data: data.map((d) => d.vendas),
          label: "Vendas",
        },
      ]}
      height={300}
    />
  );
}