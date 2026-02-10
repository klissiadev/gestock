import { useState, useEffect } from 'react'
import { Box, Typography } from "@mui/material";
import { fetchTitle } from "../services/titleFetcher";

const SessionItem = ({ id, isSelected, onSelect, updateTrigger }) => {
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

    }, [updateTrigger]);



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

export default SessionItem
