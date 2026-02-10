import { Box, Typography, IconButton } from "@mui/material";  
import BarSvg from "../../../assets/icon/iconBar.svg?react";

const ChatHeader = ({
  selectedSession,
  onToggleHistory,
  title,
}) => {
  return (
    <Box
      sx={{
        position: "relative",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        pb: 2,
        borderBottom: "1px solid",
        borderColor: "divider",
      }}
    >
      {/* Titulo centralizado */}
      <Typography fontSize={18} fontWeight={500}>
        {title || "Minerva"}
      </Typography>

      {/* BOTÃO COLADO NA DIREITA */}
      <IconButton
        onClick={onToggleHistory}
        sx={(theme) => ({
          position: "absolute",
          right: 0,
          backgroundColor: theme.palette.iconButton.active,
          borderRadius: "10px",
          "&:hover": {
            backgroundColor: theme.palette.action.hover,
          },
        })}
      >
        <BarSvg width={18} height={18} />
      </IconButton>
    </Box>
  );
};

export default ChatHeader;
