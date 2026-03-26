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
                backgroundColor: (theme) => theme.palette.iconButton.hover,
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
        background: (theme) => theme.palette.common.white,
        borderRadius: "24px",
        px: 4,
        py: 2,
        height: 355,
        width: "100%",
        boxShadow: "0 4px 20px rgba(0,0,0,0.16)",
      }}
    >
      <Typography
        sx={{ fontSize: 18, fontWeight: 500, textAlign: "center", mb: 2}}
      >
        Top vendas - {period}
      </Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {topSales.map((item) => (
          <Box key={item.product}>
            <Typography sx={{ fontSize: 12}}>
              {item.product}
            </Typography>

            <SaleTooltip product={item.product} total={item.total}>
              <Box
                sx={{
                  height: 18,
                  width: "100%",
                  background:  (theme) => theme.palette.iconButton.selected,
                  borderRadius: "20px",
                  overflow: "hidden",
                  cursor: "pointer",
                }}
              >
                <Box
                  sx={{
                    height: "100%",
                    width: `${(item.total / MAX) * 100}%`,
                    background:  (theme) => theme.palette.primary.main,
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
