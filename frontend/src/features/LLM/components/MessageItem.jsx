import React, { useMemo } from 'react'
import { Box, Avatar, IconButton, Tooltip } from '@mui/material';
import CopySvg from "../../../assets/icon/iconCopy.svg?react";
import RefrashSvg from "../../../assets/icon/iconRefrash.svg?react";
import PerfilSvg from "../../../assets/icon/iconPerfil.svg?react";
import ChatMarkdown from "./ChatMarkdown";

const MessageItem = React.memo(({ msg, isUser, handleCopy }) => {
    return (
        <Box
            sx={{
                display: "flex",
                gap: 1,
                justifyContent: isUser ? "flex-end" : "flex-start",
            }}
        >
            <Box sx={{ maxWidth: "75%", display: "flex", flexDirection: "column", alignItems: isUser ? "flex-end" : "flex-start" }}>
                <Box
                    sx={{
                        px: 2, py: 1.25,
                        borderRadius: isUser ? "12px 12px 4px 12px" : "12px 12px 12px 4px",
                        bgcolor: isUser ? "iconButton.active" : "background.paper",
                        display: "flex",
                        alignItems: "flex-end",
                    }}
                >
                    <ChatMarkdown content={msg.content} />
                </Box>

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
                        <Tooltip title="Regenerar">
                            <IconButton size="small">
                                <RefrashSvg width={14} height={14} />
                            </IconButton>
                        </Tooltip>
                    </Box>
                )}
            </Box>
        </Box>
    );
});

export default MessageItem
