import { Box, Typography } from "@mui/material";
import { LineChart } from "@mui/x-charts/LineChart";

export default function SalesLineChart({ salesByMonth }) {
  return (
    <Box
      sx={{
        p:1
      }}
    >

      <LineChart
        height={190}
        series={[
            {
            data: salesByMonth.map((d) => d.value),
            showMark: true,
            curve: "linear",
            color: "#000000", 
            },
        ]}
        xAxis={[
            {
                scaleType: "point",
                data: salesByMonth.map((d) => d.month),
                tickSize: 5, 
            },
        ]}
        yAxis={[
            {
                tickSize: 10, 
                
            },
        ]}
        grid={{ horizontal: true }}
        sx={{
            "& .MuiChartsAxis-line": {
            display: "none",
            },

            "& .MuiChartsGrid-line": {
            strokeDasharray: "4 4",
            stroke: "#cfcfcf",
            },

            "& .MuiLineElement-root": {
            strokeWidth: 2,
            },

            "& .MuiMarkElement-root": {
            strokeWidth: 2,
            r: 4,
            },
        }}
        />
    </Box>
  );
}
