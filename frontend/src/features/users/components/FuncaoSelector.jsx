import { Box, Typography } from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";

export default function FuncaoSelector({ value, onChange }) {
  const options = [
    { label: "Administrador", value: "admin" },
    { label: "PCP", value: "gestor" },
  ];

  return (
    <Box>
      <Typography fontSize={15} mb={1} mt={1}>
        Função
      </Typography>

      <Box display="flex" gap={3}>
        {options.map((option) => {
          const selected = value === option.value;

          return (
            <Box
              key={option.value}
              onClick={() => onChange(option.value)}
              sx={{
                flex: 1,
                display: "flex",
                alignItems: "center",
                gap: 2,
                px: 2,
                py: 1,
                borderRadius: "12px",
                border:"1px solid #a5a5a5",
                cursor: "pointer",
                transition: "0.2s",
                backgroundColor: "transparent",

                "&:hover": {
                  backgroundColor: "#F5F5F5",
                },
              }}
            >
              {/* Círculo */}
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  borderRadius: "50%",
                  border:  selected ? "none" : "1px solid #000",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: selected ? "#a1a1a1" : "transparent",
                }}
              >
                {selected && <CheckIcon sx={{ fontSize: 14  , color:"#d3d3d3" }} />}
              </Box>

              <Typography fontSize={14}>
                {option.label}
              </Typography>
            </Box>
          );
        })}
      </Box>
    </Box>
  );
}