
import { Box, Typography, IconButton } from "@mui/material";
import NorthEastIcon from "@mui/icons-material/NorthEast";

function StatusPill({ label }) {
  return (
    <Box
      sx={{
        bgcolor: "#919191", 
        borderRadius: "20px",
        fontSize: 12,
        textAlign: "center",
        minWidth: 60,
        ml:1
      }}
    >
      {label}
    </Box>
  );
}

export default function ExpiringItemsCard({ expiringItems }) {
  return (
    <Box
      sx={{
        background: "#EDEDED",
        borderRadius: "24px",
        py: 2,
        px:1,
        height: 440,
        width:"100%",
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          position: "relative",
          mb: 3,
        }}
      >
        <Typography sx={{ fontSize: 20, fontWeight: 500 }}>
          Itens vencendo
        </Typography>

        <IconButton
          sx={{
            position: "absolute",
            right: 10,
            bgcolor: "#c9c9c9",
            boxShadow: 2,
            borderRadius: "50%",
            height:30,
            width:30,
          }}
        >
          <NorthEastIcon />
        </IconButton>
      </Box>

      {/* Cabeçalho */}
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr 1fr 1fr",
          px: 1,
          pb: 1,
          borderBottom: "1px solid #CFCFCF",
          color: "#000000",
          justifyItems: "center"
        }}
      >
        <Typography fontSize={12} fontWeight={600}>Produto</Typography>
        <Typography fontSize={12} fontWeight={600}>Quantidade</Typography>
        <Typography fontSize={12} fontWeight={600}>Validade</Typography>
        <Typography fontSize={12} fontWeight={600}>Status</Typography>
      </Box>

      {/* Linhas */}
      <Box sx={{ mt: 2, display: "flex", flexDirection: "column", gap: 3}}>
        {expiringItems.map((item, index) => (
          <Box
            key={index}
            sx={{
              display: "grid",
              gridTemplateColumns: "2fr 1fr 1fr 1fr",
              px: 1,
              justifyItems: "center"
            }}
          >
            <Typography
                sx={{ 
                    maxWidth: 150,
                    fontSize: 16,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap"
                }}
            >
              {item.product}
            </Typography>

            <Typography sx={{ fontSize: 14 }}>{item.quantity}</Typography>

            <Typography sx={{ fontSize: 14 }}>{item.due}</Typography>

            <StatusPill label={item.status} />
          </Box>
        ))}
      </Box>
    </Box>
  );
}
