import {
  Box,
  TextField,
  IconButton,
  CircularProgress,
} from "@mui/material";
import SendIcon from "../../../assets/icon/iconUp.svg?react";

const ChatInput = ({
  value,
  onChange,
  onSend,
  disabled,
}) => {
  return (
    <Box
      sx={{
        px: 1,
        borderRadius: "12px",
        border: "1px solid",
        borderColor: "common.gray",
        backgroundColor: "background.paper",
        width: "100%",
        transition: "border-color 0.2s",
        "&:focus-within": {
          borderColor: "black",
        },
        mt: 2,
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "flex-end",
          gap: 1,
        }}
      >
        {/* INPUT CRESCE PARA CIMA */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            flexDirection: "column-reverse",
          }}
        >
          <TextField
            fullWidth
            multiline
            minRows={1}
            maxRows={3}
            variant="standard"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder="Pergunte alguma coisa..."
            disabled={disabled}
            InputProps={{ disableUnderline: true }} 
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                onSend();
              }
            }}
          />
        </Box>

        <IconButton
          onClick={onSend}
          disabled={disabled}
          sx={{
            width: 36,
            height: 36,
            flexShrink: 0,
          }}
        >
          <SendIcon width={16} height={16} />
        </IconButton>
      </Box>
    </Box>
  );
};
export default ChatInput;