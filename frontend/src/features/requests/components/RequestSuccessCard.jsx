import { Box, Typography, Button } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { useNavigate } from "react-router-dom";

const RequestSuccessCard = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        width: 360,
        p: 3,
        borderRadius: 3,
        bgcolor: "background.paper",
        boxShadow: "0 10px 30px rgba(0,0,0,0.15)",
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      {/* HEADER */}
      <Box display="flex" alignItems="center" gap={2}>
        <CheckCircleIcon
          sx={{
            fontSize: 28,
            color: "primary.main",
          }}
        />

        <Typography fontSize={18} fontWeight={500}>
          Requisição enviada
        </Typography>
      </Box>

      {/* TEXTO */}
      <Typography fontSize={14} color="text.secondary">
        Requisição enviada com sucesso!
        <br />
        A requisição já pode ser visualizada.
      </Typography>

      {/* BOTÕES */}
      <Box display="flex" gap={1} mt={1}>
        <Button
          variant="outlined"
          fullWidth
          onClick={() => navigate("/requests")}
        >
          Visualizar
        </Button>

        <Button
          variant="contained"
          fullWidth
          onClick={() => navigate("/requests")}
        >
          Concluído
        </Button>
      </Box>
    </Box>
  );
};

export default RequestSuccessCard;