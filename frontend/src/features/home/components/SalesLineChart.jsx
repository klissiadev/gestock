import { Box, Typography } from "@mui/material";
import { LineChart } from "@mui/x-charts/LineChart";

export default function SalesLineChart({ salesByMonth }) {
  return (
    <Box
      sx={{
        width: "100%",
        backgroundColor: "#efefef",
        borderRadius: 3,
        p: 1,
      }}
    >
      <Typography
        fontSize={18}
        textAlign="center"
        sx={{ mb: 2, fontWeight: 500 }}
      >
        Meses com mais vendas
      </Typography>

      <LineChart
        height={220}
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
