import { Box, Typography } from "@mui/material";
import { useEffect, useState, memo } from "react";
import { fetchTitle } from "../services/titleFetcher";

const SessionItem = ({ id, title, isSelected, onSelect, updateTrigger }) => {
    const [titulo, setTitulo] = useState(title);

    useEffect(() => {
        const loadTitle = async () => {
            if (title && !updateTrigger) return;

            const token = localStorage.getItem('token');
            if (!id || !token) return;

            try {
                const data = await fetchTitle(id, token);
                console.log("Titulo definido: ", data);
                setTitulo(data);
            } catch (error) {
                console.error("Erro ao buscar título:", error);
            }
        };

        loadTitle();
    }, [id, updateTrigger]);

    useEffect(() => {
        if (title) setTitulo(title);
    }, [title]);

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
                {titulo || "Nova conversa"}
            </Typography>
        </Box>
    );
};

export default memo(SessionItem);
