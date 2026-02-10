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
import ChatContainer from "./components/ChatContainer";
import ChatInput from "./components/ChatInput";
import FAQSuggestions from "./components/FAQSuggestions";
import InitialChatLayout from "./components/InitialChatLayout";
import ChatHistorySide from "./components/ChatHistorySide";

import { fetchTitle } from "./services/titleFetcher";
import InitalPage from "./pages/InitalPage";
import ChatModule from "./pages/ChatModule";

const LLMPage = () => {
  const [title, setTitle] = useState("Minerva");
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const location = useLocation();
  const [historyOpen, setHistoryOpen] = useState(false);
  const [streamingId, setStreamingId] = useState(null);
  const [updateTrigger, setUpdateTrigger] = useState(false); // Novo estado para forçar atualização do título

  useEffect(() => {
    loadSessions();
  }, []);

  // Gerador de titulo
  useEffect(() => {
    const loadTitle = async () => {
      try {
        if (!selectedSession) return;

        const sessionTitle = await fetchTitle(selectedSession);
        setTitle(sessionTitle || "Nova Conversa");
      } catch (error) {
        console.error("Falha ao recuperar título:", error);
        setTitle("Nova Conversa");
      }
    };

    loadTitle();
  }, [selectedSession]);


  useEffect(() => {
    const initFromNavigation = async () => {
      const { sessionId } = location.state || {};
      if (!sessionId) return;

      setSelectedSession(sessionId);

      // ESSENCIAL
      await loadSessions();
    };

    initFromNavigation();
  }, [location.state]);


  useEffect(() => {
    const loadMessages = async () => {
      if (!selectedSession) return;

      const history = await fetchSessionMessages(selectedSession);

      setMessages(
        history.map((msg) => ({
          id: crypto.randomUUID(),
          role: msg.role,
          content: msg.content,
        }))
      );
    };

    loadMessages();
  }, [selectedSession]);



  const loadSessions = async () => {
    setLoadingSessions(true);
    try {
      const data = await fetchSessions();
      setSessions(data || []);
    } catch (err) {
      console.error("Erro ao carregar sessões:", err);
    } finally {
      setLoadingSessions(false);
    }
  };

  const handleCreateSession = async () => {
    const sessionId = await createSession();
    await loadSessions();
    setSelectedSession(sessionId);
  };

  const handleSend = async () => {
    if (!input.trim() || !selectedSession) return;

    const messageToSend = input;
    setInput("");
    setLoading(true);

    const assistantId = crypto.randomUUID();


    // adiciona user + assistant vazio juntos (importante)
    setMessages((prev) => [
      ...prev,
      { role: "user", content: messageToSend },
      { id: assistantId, role: "assistant", content: "" },
    ]);

    let fullMessage = "";

    try {
      await streamMessageToLLM(
        messageToSend,
        selectedSession,
        (chunk) => {
          fullMessage += chunk;

          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantId
                ? { ...msg, content: fullMessage }
                : msg
            )
          );
        }
      );

      // Atualiza o título após a resposta completa (se o titulo for nulo)
      if (title === "Nova Conversa") {
        setTimeout(async () => {
          const newTitle = await fetchTitle(selectedSession);

          if (newTitle) { setTitle(newTitle); setUpdateTrigger(prev => !prev); }
        }, 1000);
      }



    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Erro ao comunicar com a LLM." },
      ]);
    } finally {
      setLoading(false);
    }

  };


  return (
    <Box
      sx={{
        height: "80vh",
        display: "flex",
        flexDirection: "row",   // 👈 AGORA É LADO A LADO
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
          sessions={sessions}
          selectedSession={selectedSession}
          onSelectSession={setSelectedSession}
          onCreateSession={handleCreateSession}
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
                  handleSend={handleSend}
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
                  loading={loading}/>

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
        onCreateSession={handleCreateSession}
        updateTrigger={updateTrigger}
      />
    </Box>
  );
};

export default LLMPage;
