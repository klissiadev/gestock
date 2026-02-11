import {
  Box,
} from "@mui/material";

import MessageItem from "./MessageItem";
import { useCallback } from "react";


const ChatMessages = ({ messages }) => {
  const handleCopy = useCallback((text) => {
    navigator.clipboard.writeText(text);
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        gap: 2,
      }}
    >

      {messages.map(
        (msg) => (
          <MessageItem
            key={msg.id}
            msg={msg}
            isUser={msg.role === "user"}
            handleCopy={handleCopy}
          />
        )
      )}

    </Box>
  );
};

export default ChatMessages;
