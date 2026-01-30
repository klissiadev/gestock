import {
  Typography,
  Box,
  IconButton,
  Avatar,
  Tooltip,
} from "@mui/material";

import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import ReplayIcon from "@mui/icons-material/Replay";

import CopySvg from "../../../assets/icon/iconCopy.svg?react";
import RefrashSvg from "../../../assets/icon/iconRefrash.svg?react";
import PerfilSvg from "../../../assets/icon/iconPerfil.svg?react";


const ChatMessages = ({ messages }) => {
  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        gap: 2,
        mb: 12,
        px: {
          sm: 4,
          md: 14,
          lg: 24,  
        },
      }}
    >
      {messages.map((msg, idx) => {
        const isUser = msg.role === "user";

        return (
          <Box
            key={idx}
            sx={{
              display: "flex",
              gap: 1,
              justifyContent: isUser ? "flex-end" : "flex-start",
            }}
          >
            

            <Box 
              sx={{
                maxWidth: "75%",
                display: "flex",
                flexDirection: "column",
                alignItems: isUser ? "flex-end" : "flex-start",
              }}

            >
              {/* Balão */}
              <Box
                sx={{
                  px: 2,
                  py: 1.25,
                  borderRadius: isUser
                    ? "12px 12px 4px 12px"
                    : "12px 12px 12px 4px",
                  bgcolor: isUser ? "iconButton.active" : null ,
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                  display: "flex",
                  alignItems: "flex-end",
                }}
              >
                <Typography
                  sx={{
                    fontSize: "0.95rem",
                    lineHeight: 1.6,
                    fontWeight: 300,
                  }}
                >
                  {msg.content}
                </Typography>
              </Box>
              
              {/* Avatar Usuário */}
              {isUser && (
                <Avatar
                  sx={{
                    width: 24,
                    height: 24,
                    fontSize: 14,
                    bgcolor: "iconButton.active",
                    mt: 0.5,
                  }}
                >
                  <PerfilSvg width={14} height={14} />
                </Avatar>
              )}

              {/* Ações da LLM */}
              {!isUser && (
                <Box
                  sx={{
                    mt: 0.5,
                    display: "flex",
                    gap: 0.5,
                    opacity: 0.6,
                  }}
                >
                  <Tooltip title="Copiar">
                    <IconButton
                      size="small"
                      onClick={() => handleCopy(msg.content)}
                    >
                      <CopySvg width={16} height={16} />
                    </IconButton>
                  </Tooltip>

                  <Tooltip title="Regenerar">
                    <IconButton size="small">
                      <RefrashSvg width={14} height={14} />
                    </IconButton>
                  </Tooltip>
                </Box>
              )}
            </Box>

            
          </Box>
        );
      })}
    </Box>
  );
};

export default ChatMessages;
