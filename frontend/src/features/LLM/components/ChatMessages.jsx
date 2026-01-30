import { Typography, Box } from "@mui/material";

const ChatMessages = ({ messages }) => {
  return (
    <>
      {messages.map((msg, idx) => (
        <Box key={idx} sx={{ mb: 1 }}>
          <Typography
            sx={{
              fontWeight: msg.role === "user" ? 600 : 400,
            }}
          >
            {msg.role === "user" ? "Você: " : "LLM: "}
            {msg.content}
          </Typography>
        </Box>
      ))}
    </>
  );
};

export default ChatMessages;
