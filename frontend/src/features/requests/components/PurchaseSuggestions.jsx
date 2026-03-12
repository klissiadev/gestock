import { Box, Typography, Chip} from "@mui/material";
import LampSvg from "../../../assets/icon/iconLamp.svg?react";

const PurchaseSuggestions = ({ onSelectSuggestion, suggestions }) => {
  return (
    <Box
      sx={{
        mt: 3,
        width: "100%",
        p: 2,
        borderRadius: 2,
        bgcolor: "grey.50",
        boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
      }}
    >
      {/* HEADER */}
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <LampSvg style={{ width: 16, height: 16 }} />

        <Typography fontSize={14} fontWeight={500}>
          Sugestões de compra
        </Typography>
      </Box>

      <Box display="flex" flexWrap="wrap" gap={1}>
        {suggestions.map((product) => (
          <Box
            key={product.id}
            sx={{
              flexBasis: "calc(50% - 4px)",
              position: "relative",
            }}
          >
            {/* BADGE DE QUANTIDADE */}
            <Box
              sx={{
                position: "absolute",
                top: 6,
                right: 6,
                bgcolor: (theme) => theme.palette.iconButton.active,
                color: "white",
                fontSize: 11,
                px: 1,
                py: "2px",
                borderRadius: 1,
                fontWeight: 600,
              }}
            >
              x{product.qty}
            </Box>
              <Chip
                onClick={() => onSelectSuggestion(product)}
                sx={{
                  width: "100%",
                  height: "auto",
                  borderRadius: 2,
                  cursor: "pointer",
                  justifyContent: "flex-start",
                  alignItems: "flex-start",
                  p: 1,

                  "& .MuiChip-label": {
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "flex-start",
                    gap: "2px",
                    whiteSpace: "normal",
                  },
                }}
                label={
                  <>
                    <Typography fontSize={13} fontWeight={500}>
                      {product.name}
                    </Typography>

                    <Typography
                      fontSize={11}
                      color="text.secondary"
                      sx={{
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                        maxWidth: "100%",
                      }}
                    >
                      {product.description}
                    </Typography>
                  </>
                }
              />
          </Box>
        ))}
      </Box>
    </Box>
  );
};

export default PurchaseSuggestions;