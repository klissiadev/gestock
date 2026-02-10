import { Box, Typography, IconButton, Divider, Button} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import AddSvg from "../../../assets/icon/iconAdd.svg?react";
import { fetchTitle } from "../services/titleFetcher";
import {useState, useEffect } from 'react';



// --- SUBCOMPONENTE DE ITEM (Unificado no mesmo arquivo) ---
const SessionItem = ({ id, isSelected, onSelect }) => {
  const [title, setTitle] = useState(null);

  useEffect(() => {
    const loadTitle = async () => {
      try {
        const data = await fetchTitle(id);
        setTitle(data);
      } catch (error) {
        console.error("Erro no título:", error);
      }
    };
    if (id) loadTitle();
  }, [id]);

  const displayTitle = title || "Nova conversa";

  return (
    <Box
      onClick={() => onSelect(id)}
      sx={{
        p: "10px 12px",
        mb: 0.5,
        borderRadius: "8px",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        gap: 1.5,
        bgcolor: isSelected ? "action.selected" : "transparent",
        "&:hover": { bgcolor: "action.hover", color: "text.primary" },
        transition: "all 0.2s ease",
      }}
    >
      <Typography
        variant="body2"
        sx={{
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
          fontSize: "0.85rem",
          fontWeight: isSelected ? 600 : 400,
        }}
      >
        {displayTitle}
      </Typography>
    </Box>
  );
};


const ChatHistorySide = ({
  open,
  onClose,
  sessions,
  selectedSession,
  onSelectSession,
  onCreateSession,
}) => {


  


  return (
    <Box
      sx={(theme)=>({
        width: open ? 320 : 0,
        transition: "width .3s ease",
        overflow: "hidden",
        borderRadius: 2,
        display: "flex",
        flexDirection: "column",
        bgcolor: theme.palette.iconButton.hover,
      })}
    >
      <Box
        sx={{
          opacity: open ? 1 : 0,
          transition: "opacity .2s ease",
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          p={2}
        >
          <Typography fontWeight={500} color="textDisabled">Histórico</Typography>
          <IconButton onClick={onClose} 
            sx={(theme) => ({
              width: 30,
              height: 30,
              borderRadius: '50%',
              backgroundColor: theme.palette.iconButton.active,
              color:"black"
            })}
          >
            <CloseIcon />
          </IconButton>
        </Box>

        {/* BOTÃO NOVO CHAT */}
        <Box px={2} pb={2}>
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={<AddSvg width={18} height={18} />}
            onClick={() => {
              onCreateSession();
              onClose();
            }}
            sx={{ 
              textTransform: 'none', 
              borderColor: 'common.black',
              fontSize: 14,
              borderRadius: '12px',
              fontWeight: 500,
              width: '100%'
            }}
          > Nova conversa</Button>
        </Box>

        <Divider />

        <Box sx={{ overflowY: "auto", p: 1 }}>


          {sessions.map((s) => {
            const id = typeof s === "string" ? s : s.session_id;
            return (
              <SessionItem
                key={id}
                id={id}
                isSelected={id === selectedSession}
                onSelect={onSelectSession}
              />
            );
          })}


        </Box>
      </Box>
    </Box>
  );
};

export default ChatHistorySide;
