import {
  Box,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Divider,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import AddIcon from "@mui/icons-material/Add";
import { useState } from "react";

const ChatHeader = ({
  sessions,
  selectedSession,
  onSelectSession,
  onCreateSession,
}) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleOpen = (e) => {
    setAnchorEl(e.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSelect = (id) => {
    onSelectSession(id);
    handleClose();
  };

  const handleToggle = (e) => {
    e.stopPropagation();
    setAnchorEl(e.currentTarget);
  };

  return (
    <Box
      sx={{
        display: "flex",
        gap: 1,
        mb: 2,
        cursor: "pointer",
        pb: 2,
        borderBottom: "1px solid",
        borderColor: "divider",
        width: "100%",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Box
        display="flex"
        alignItems="center"
        gap={0.5}
        onClick={handleToggle}
      >
        <Typography fontSize={16}>
          {selectedSession ? "Nome do chat" : "Nova conversa"}
        </Typography>

        <ExpandMoreIcon fontSize="small" />
      </Box>

      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        PaperProps={{
          sx: { minWidth: 220 },
        }}
      >
        {sessions.map((s) => {
          const sessionId =
            typeof s === "string" ? s : s.session_id;

          return (
            <MenuItem
              key={sessionId}
              onClick={() => handleSelect(sessionId)}
            >
              {sessionId}
            </MenuItem>
          );
        })}

        <Divider />

        <MenuItem
          onClick={() => {
            handleClose();
            onCreateSession();
          }}
        >
          <AddIcon fontSize="small" sx={{ mr: 1 }} />
          Nova conversa
        </MenuItem>
      </Menu>
    </Box>

  );
};

export default ChatHeader;
