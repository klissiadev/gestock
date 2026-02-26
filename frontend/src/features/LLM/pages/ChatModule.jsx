import React from 'react'
import ChatContainer from '../components/ChatContainer'
import { Box } from '@mui/material'
import ChatInput from '../components/ChatInput'

const ChatModule = ({ messages, input, setInput, handleSend, selectedSession, loading}) => {
    return (
        <>
            <ChatContainer messages={messages} loading={loading} />
            <Box sx={{ mt: "auto", }}>
                <ChatInput
                    value={input}
                    onChange={setInput}
                    onSend={handleSend}
                    disabled={!selectedSession || loading}
                />
            </Box>
        </>
    )
}

export default ChatModule
