import {
  Box,
  Typography,
} from "@mui/material";
import SentimentSatisfiedIcon from '@mui/icons-material/SentimentSatisfied';

const InitialChatLayout = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        gap: 1,
        position: "relative",
        mb: 6,
      }}
    >
      {/* Ícone */}
      <Box
        sx={{
          width: 40,
          height: 40,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          mb: 1,
          borderRadius: '12px',
          border: '1.5px solid',
          borderColor: 'divider',
        }}
      >
        <SentimentSatisfiedIcon color="black" />
      </Box>

      <Typography variant="body2" color="text.secondary">
        Olá! Tudo bem?
      </Typography>

      <Typography variant="h5" fontWeight={600}>
        Como podemos te ajudar?
      </Typography>
    </Box>
  );
};

export default InitialChatLayout;
