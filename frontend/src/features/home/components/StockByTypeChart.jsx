// StockByTypeChart.jsx
import { Box, Typography } from "@mui/material";
import { BarChart } from "@mui/x-charts/BarChart";


export default function StockByTypeChart({ stockByType, period }) {
  return (
    <Box
      sx={{
        background: "#EDEDED",
        borderRadius: "24px",
        py: 2,
        height: 440,
        width:"100%",

        "& .MuiChartsGrid-line": {
          strokeDasharray: "6 6",
          stroke: "#BDBDBD",
        },
        "& .MuiChartsAxis-line": {
          display: "none",
        },
        "& .MuiBarElement-root": {
          rx: 20,
          ry: 24,
        },
      }}
    >
      <Typography
        sx={{
          fontSize: 20,
          fontWeight: 500,
          textAlign:"center",
          py:1
        }}
      >
        Estoque por tipo - {period}
      </Typography>

      <BarChart
        dataset={stockByType}
        xAxis={[
          {
            scaleType: "band",
            dataKey: "label",
            tickLabelStyle: {
              fontSize: 12,
              fill: "#000",
            },
            axisLine: { stroke: "transparent" },
            tickSize: 5,
            bandPadding: 0.6, 
          },
        ]}
        yAxis={[
          {
            min: 0,
            max: 600,
            tickNumber: 7,
            tickLabelStyle: {
              fontSize: 14,
              fill: "#555",
            },
            axisLine: { stroke: "transparent" },
            tickSize: 10,
            grid: {
              stroke: "#BDBDBD",
              strokeDasharray: "6 6",
            },
          },
        ]}
        series={[
          {
            dataKey: "value",
            color: "#222626",
          },
        ]}
        margin={{ top: 20, bottom: 60, left: 20, right: 20 }}
        borderRadius={18}
        grid={{ horizontal: true, vertical: false}}
        slotProps={{
          legend: { hidden: true },
        }}
        categoryGapRatio={0.65}
      />
    </Box>
  );
}
