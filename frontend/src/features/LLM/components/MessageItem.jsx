import React, { useMemo } from 'react';
import { Box, Avatar, IconButton, Tooltip } from '@mui/material';
import CopySvg from "../../../assets/icon/iconCopy.svg?react";
import RefrashSvg from "../../../assets/icon/iconRefrash.svg?react";
import PerfilSvg from "../../../assets/icon/iconPerfil.svg?react";
import ChatMarkdown from "./ChatMarkdown";
import ReportTable from "./ReportTable"; // Importe o novo componente

import { parsePartialReport } from '../services/parserjson';

const MessageItem = React.memo(({ msg, isUser, handleCopy }) => {

    // Lógica para detectar se a mensagem é um relatório estruturado
    const reportData = useMemo(() => {
        if (isUser || !msg.content) return null;

        // Usa a nova função de parse que aceita JSON incompleto
        return parsePartialReport(msg.content);
    }, [msg.content, isUser]);

    return (
        <Box
            sx={{
                display: "flex",
                gap: 1,
                justifyContent: isUser ? "flex-end" : "flex-start",
                mb: 2
            }}
        >
            <Box sx={{
                maxWidth: reportData ? "90%" : "75%", // Relatórios ganham mais largura
                display: "flex",
                flexDirection: "column",
                alignItems: isUser ? "flex-end" : "flex-start"
            }}>
                <Box
                    sx={{
                        px: 2, py: 1.25,
                        borderRadius: isUser ? "12px 12px 4px 12px" : "12px 12px 12px 4px",
                        bgcolor: isUser ? "iconButton.active" : "background.paper",
                        width: reportData ? '100%' : 'auto', // Ajusta largura se for relatório
                        boxShadow: reportData ? 1 : 0, // Leve sombra para destacar tabelas
                    }}
                >
                    {reportData ? (
                        <ReportTable
                            reportType={reportData.report_type}
                            payload={reportData.payload}
                            metadata={reportData.metadata}
                        />
                    ) : (
                        <ChatMarkdown content={msg.content} />
                    )}
                </Box>

                {/* Área de Ações (Avatar/Botões) */}
                {isUser ? (
                    <Avatar sx={{ width: 24, height: 24, mt: 0.5, bgcolor: "iconButton.active" }}>
                        <PerfilSvg width={14} height={14} />
                    </Avatar>
                ) : (
                    <Box sx={{ mt: 0.5, display: "flex", gap: 0.5, opacity: 0.6 }}>
                        <Tooltip title="Copiar">
                            <IconButton size="small" onClick={() => handleCopy(msg.content)}>
                                <CopySvg width={16} height={16} />
                            </IconButton>
                        </Tooltip>
                        {!reportData && ( // Oculta regenerar em relatórios se preferir
                            <Tooltip title="Regenerar">
                                <IconButton size="small">
                                    <RefrashSvg width={14} height={14} />
                                </IconButton>
                            </Tooltip>
                        )}
                    </Box>
                )}
            </Box>
        </Box>
    );
});

export default MessageItem;