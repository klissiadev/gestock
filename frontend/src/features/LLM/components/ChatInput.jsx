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
  loading,
}) => {
  return (
    <Box
      sx={{
        mt: 2,
        px: 1,
        borderRadius: "12px",
        border: "1px solid",
        borderColor: "black",
        display: "flex",
        alignItems: "flex-end",
        gap: 1,
        backgroundColor: "background.paper",
        width: "100%",
        transition: "border-color 0.2s",
        "&:focus-within": {
          borderColor: "primary.main",
        },
      }}
    >
      <TextField
        fullWidth
        multiline
        maxRows={4}
        variant="standard"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Pergunte alguma coisa..."
        disabled={disabled}
        InputProps={{
          disableUnderline: true,
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSend();
          }
        }}
        sx={{
          px: 0.5,
          "& .MuiInputBase-input": {
            color: "text.primary",
            fontWeight: 400,     
            fontSize: "0.95rem",
            lineHeight: 1.5,
          },
          "& .MuiInputBase-input::placeholder": {
            color: "text.secondary",
            opacity: 1,
            fontWeight: 400,
          },
        }}
      />

      <IconButton
        onClick={onSend}
        disabled={disabled}
        sx={{
          bgcolor: "primary.main",
          color: "primary.contrastText",
          "&:hover": {
            bgcolor: "primary.dark",
          },
          width: 36,
          height: 36,
          flexShrink: 0, // Prevent shrinking
        }}
      >
        {loading ? (
          <CircularProgress size={18} color="inherit" />
        ) : (
          <SendIcon width={16} height={16} />
        )}
      </IconButton>
    </Box>
  );
};

export default ChatInput;
