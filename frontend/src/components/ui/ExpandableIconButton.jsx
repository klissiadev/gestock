import { Box, Typography } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useChatSession } from "../../ChatSessionContext";
import { createSession, sendMessageToLLM } from "../../api/LLMAPI";

export default function ExpandableIconButton({
  icon,
  label = "Minerva",
  origin,
  initialMessage,
}) {
  const [hover, setHover] = useState(false);
  const navigate = useNavigate();
  const { getSession, setSession } = useChatSession();

  const handleClick = async () => {

    let sessionId = getSession(origin);
  

    if (!sessionId) {
      sessionId = await createSession();
      setSession(origin, sessionId);

      if (initialMessage) {
        await sendMessageToLLM(initialMessage, sessionId);
      }
    }

    navigate("/ai", {
      state: { sessionId },
    });
  };

  return (
    <Box
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onClick={handleClick}
      sx={(theme) => ({
        height: 48,
        width: hover ? 160 : 48,
        backgroundColor: theme.palette.iconButton.active,
        borderRadius: "12px",
        display: "flex",
        alignItems: "center",
        cursor: "pointer",
        overflow: "hidden",
        transition:
          "width 250ms cubic-bezier(0.4, 0, 0.2, 1), background-color 150ms",
        "&:hover": {
          backgroundColor: theme.palette.iconButton.hover,
        },
      })}
    >
      <Box
        sx={(theme) => ({
          minWidth: 48,
          height: 48,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          borderRadius: "12px",
          backgroundColor: theme.palette.iconButton.active,
        })}
      >
        {icon}
      </Box>

      <Typography
        sx={{
          whiteSpace: "nowrap",
          opacity: hover ? 1 : 0,
          transform: hover ? "translateX(0)" : "translateX(-12px)",
          transition: "all 200ms ease",
          fontSize: 18,
          fontWeight: 500,
          marginLeft: 2,
        }}
      >
        {label}
      </Typography>
    </Box>
  );
}
