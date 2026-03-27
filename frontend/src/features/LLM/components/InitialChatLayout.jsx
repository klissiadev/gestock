import {
  Box,
  Typography,
} from "@mui/material";
import ChatActiveSvg from "../../../assets/icon/icon-minerva-purple.svg?react";

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
          width: 50,
          height: 50,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          mb: 1,
          borderRadius: '12px',
          boxShadow: "6px 6px 8px rgba(80, 9, 126, 0.5)",
        }}
      >
        <ChatActiveSvg/>
      </Box>

      <Typography variant="body2" color="text.secondary">
        Olá! Tudo bem?
      </Typography>

      <Typography variant="h5" fontWeight={600}>
        Como posso te ajudar?
      </Typography>
    </Box>
  );
};

export default InitialChatLayout;
