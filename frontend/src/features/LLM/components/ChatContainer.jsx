import { Paper, Typography } from "@mui/material";
import ChatMessages from "./ChatMessages";

const ChatContainer = ({ messages }) => {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 2,
        minHeight: 300,
        maxHeight: 400,
        overflowY: "auto",
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
