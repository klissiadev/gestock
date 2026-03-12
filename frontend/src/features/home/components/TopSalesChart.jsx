// TopSalesManual.jsx
import { Box, Typography, Tooltip, Paper, Divider } from "@mui/material";

const MAX = 700;

function SaleTooltip({ product, total, children }) {
  return (
    <Tooltip
      arrow
      placement="top-start"
      slotProps={{
        tooltip: {
          sx: {
            bgcolor: "transparent",
            p: 0,
            boxShadow: "none",
          },
        },
        arrow: {
          sx: {
            color: "transparent",
          },
        },
      }}
      title={
        <Paper
          elevation={3}
          sx={{
            p: 1,
            borderRadius: "4px",
            minWidth: 90,
          }}
        >
          <Typography sx={{ fontSize: 14}}>{product}</Typography>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <Box
              sx={{
                width: 12,
                height: 12,
                bgcolor: "#222626",
                borderRadius: "3px",
              }}
            />
            <Typography sx={{ fontSize: 18, fontWeight: 600 }}>
              {total}
            </Typography>
          </Box>
        </Paper>
      }
    >
      {children}
    </Tooltip>
  );
}

export default function TopSalesManual({ topSales, period }) {
  return (
    <Box
      sx={{
        background: "#EDEDED",
        borderRadius: "24px",
        px: 4,
        py: 2,
        height: 300,
        width: "100%",
      }}
    >
      <Typography
        sx={{ fontSize: 18, fontWeight: 500, textAlign: "center", mb: 2}}
      >
        Top vendas - {period}
      </Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
        {topSales.map((item) => (
          <Box key={item.product}>
            <Typography sx={{ fontSize: 12}}>
              {item.product}
            </Typography>

            <SaleTooltip product={item.product} total={item.total}>
              <Box
                sx={{
                  height: 16,
                  width: "100%",
                  background: "#9E9E9E",
                  borderRadius: "20px",
                  overflow: "hidden",
                  cursor: "pointer",
                }}
              >
                <Box
                  sx={{
                    height: "100%",
                    width: `${(item.total / MAX) * 100}%`,
                    background: "#222626",
                    borderRadius: "20px",
                    transition: "0.3s",
                  }}
                />
              </Box>
            </SaleTooltip>
          </Box>
        ))}
      </Box>

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          mt: 2,
          px: 1,
        }}
      >
        {[0, 100, 200, 300, 400, 500, 600, 700].map((n) => (
          <Typography key={n} sx={{ fontSize: 12, color: "#000" }}>
            {n}
          </Typography>
        ))}
      </Box>
    </Box>
  );
}
