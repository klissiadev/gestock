import { Paper, Typography, Fab, Box } from "@mui/material";
import KeyboardArrowDownRoundedIcon from "@mui/icons-material/KeyboardArrowDownRounded";
import { useEffect, useRef, useState } from "react";
import ChatMessages from "./ChatMessages";
import LoadingComponent from "./LoadingComponent";

const ChatContainer = ({ messages, loading }) => {
  const containerRef = useRef(null);
  const bottomRef = useRef(null);
  const [showScrollButton, setShowScrollButton] = useState(false);

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Auto scroll quando novas mensagens chegam
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Detecta se usuário subiu o scroll
  const handleScroll = () => {
    const el = containerRef.current;
    if (!el) return;

    const isAtBottom =
      el.scrollHeight - el.scrollTop - el.clientHeight < 20;

    setShowScrollButton(!isAtBottom);
  };

  return (
    <Paper
      ref={containerRef}
      onScroll={handleScroll}
      sx={{
        position: "relative",
        p: 2,
        height: "100%",
        overflowY: "auto",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        gap: 2,
        boxShadow: "none",
      }}
    >
      {messages.length === 0 ? (
        <Typography color="text.secondary">
          Nenhuma mensagem ainda.
        </Typography>
      ) : (
        <>
          <ChatMessages messages={messages} />
          {/* O LoadingComponent entra aqui! */}
          {loading && (
            <Box sx={{ mt: 1, ml: 1 }}>
              <LoadingComponent />
            </Box>
          )}
          <div ref={bottomRef} />
        </>
      )}

      {showScrollButton && (
        <Fab
          size="small"
          onClick={scrollToBottom}
          sx={{
            position: "fixed",
            bottom: 150,
            left: "50%",
            transform: "translateX(-50%)",
            boxShadow: "none",
          }}
        >
          <KeyboardArrowDownRoundedIcon />
        </Fab>
      )}
    </Paper>
  );
};

export default ChatContainer;
