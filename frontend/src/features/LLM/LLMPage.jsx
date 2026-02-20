import { useEffect, useState } from "react";
import { Box } from "@mui/material";
import { useLocation } from "react-router-dom";



import {
  fetchSessions,
  createSession,
  fetchSessionMessages,
  streamMessageToLLM
} from "../../api/LLMAPI";

import ChatHeader from "./components/ChatHeader";
import ChatHistorySide from "./components/ChatHistorySide";

import { fetchTitle } from "./services/titleFetcher";
import InitalPage from "./pages/InitalPage";
import ChatModule from "./pages/ChatModule";

import { useAuth } from "../../AuthContext";
import { useMinerva } from "./services/useMinerva";

const LLMPage = () => {
  const location = useLocation();
  const { user } = useAuth();
  const [historyOpen, setHistoryOpen] = useState(false);


  const {
    sessions, selectedSession, setSelectedSession,
    messages, loading, title, updateTrigger,
    loadSessions, createNewSession, loadMessages, sendMessage,
    handleSend, input, setInput
  } = useMinerva();

  // Inicialização: Carrega sessões ao montar a página
  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  // Navegação: Se vier de outro lugar com um ID de sessão
  useEffect(() => {
    const { sessionId } = location.state || {};
    if (sessionId) {
      setSelectedSession(sessionId);
      loadSessions();
    }
  }, [location.state, setSelectedSession, loadSessions]);

  // Sincronização: Carrega mensagens sempre que a sessão mudar
  useEffect(() => {
    if (selectedSession) {
      loadMessages(selectedSession);
    }
  }, [selectedSession, loadMessages]);

  // Proteção de rota simples
  if (!user && !localStorage.getItem('token')) {
    return <InitalPage />;
  }


  return (
    <Box
      sx={{
        height: "80vh",
        display: "flex",
        flexDirection: "row",
        width: "100%",
        overflow: "hidden",
      }}
    >

      {/* CHAT */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          p: 1,
          transition: "all .3s ease",
        }}
      >
        {/* Cabecalho do chat */}
        <ChatHeader
          onToggleHistory={() => setHistoryOpen((prev) => !prev)}
          title={title}
        />

        {/* CORPO DO CHAT */}
        <Box
          sx={{
            flex: 1,
            minHeight: 0,
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* ÁREA DAS MENSAGENS */}
          <Box
            sx={{
              flex: 1,
              minHeight: 0,
              display: "flex",
              justifyContent: "center",

            }}
          >
            {/* SLOT COM ALTURA FIXA E SCROLL */}
            <Box
              sx={{
                width: "100%",
                maxWidth: messages.length === 0 ? 900 : "100%", // Tamanho condicional: Tela inicial -> 900px, Chat -> 100%
                height: "100%",
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
              }}
            >
              {messages.length === 0 ? (
                // LAYOUT INICIAL PARA QUANDO NÃO HOUVER MENSAGENS
                <InitalPage
                  input={input}
                  setInput={setInput}
                  handleSend={sendMessage}
                  loading={loading}
                />
              ) : (
                // LAYOUT DO CHAT PROPRIAMENTE DITO
                <ChatModule
                  messages={messages}
                  input={input}
                  setInput={setInput}
                  handleSend={handleSend}
                  selectedSession={selectedSession}
                  loading={loading} />
              )}
            </Box>
          </Box>
        </Box>
      </Box>

      {/* HISTÓRICO menu que abre*/}
      <ChatHistorySide
        open={historyOpen}
        onClose={() => setHistoryOpen(false)}

        sessions={sessions}
        selectedSession={selectedSession}
        onSelectSession={setSelectedSession}
        onCreateSession={createNewSession}
        updateTrigger={updateTrigger}
      />
    </Box>
  );
};

export default LLMPage;
