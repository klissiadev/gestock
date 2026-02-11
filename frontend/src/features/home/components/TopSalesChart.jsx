// TopSalesChart.jsx
import { Box, Typography } from "@mui/material";
import { BarChart } from "@mui/x-charts/BarChart";

export default function TopSalesChart({ topSales , period }) {
  return (
    <Box
      sx={{
        background: "#EDEDED",
        borderRadius: "24px",
        py:2,
        height: 440,

        "& .MuiChartsAxis-line": {
          display: "none",
        },
        "& .MuiBarElement-root": {
          rx: 18,
          ry: 18,
        },
      }}
    >
      <Typography
        sx={{
          fontSize: 20,
          fontWeight: 500,
          textAlign: "center",
          py:1
        }}
      >
        Top vendas - {period}
      </Typography>

      <BarChart
        layout="horizontal"
        dataset={topSales}
        xAxis={[
          {
            min: 0,
            max: 700,
            tickNumber: 8,
            tickLabelStyle: { fontSize: 12   },
            tickSize: 0,
          },
        ]}
        yAxis={[
          {
            scaleType: "band",
            data: topSales.map((d) => d.product),
            tickLabelStyle: {
              fontSize: 14,
              fill: "#000",
            },
            bandPadding: 0.5,
          },
        ]}
        series={[
          {
            dataKey: "total",
            color: "#222626",
          },
        ]}
        margin={{ top: 10, bottom: 40, left: 30, right: 30 }}
        grid={{ horizontal: false, vertical: false }}
      />
    </Box>
  );
}
