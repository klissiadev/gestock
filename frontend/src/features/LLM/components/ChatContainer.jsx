import { Paper, Typography } from "@mui/material";
import ChatMessages from "./ChatMessages";

const ChatContainer = ({ messages }) => {
  return (
    <Paper
    
      sx={{
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
        <ChatMessages messages={messages} />
      )}
    </Paper>
  );
};

export default ChatContainer;
