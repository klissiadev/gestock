import React from 'react'
import { Box } from '@mui/material';
import InitialChatLayout from '../components/InitialChatLayout';
import ChatInput from '../components/ChatInput';
import FAQSuggestions from '../components/FAQSuggestions';

const InitalPage = ({ input, setInput, handleSend, loading }) => {
    return (
        <Box
            sx={{
                margin: "auto",
                width: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 2,
            }}
        >
            <InitialChatLayout />
            <ChatInput
                value={input}
                onChange={setInput}
                onSend={handleSend}
                disabled={loading}
            />
            <FAQSuggestions
                onSelectSuggestion={(text) => handleSend(text)}
            />
        </Box>
    )
}

export default InitalPage
