import { useEffect, useState } from "react";
import { Box} from "@mui/material";
import { useLocation } from "react-router-dom";

import {
  fetchSessions,
  createSession,
  sendMessageToLLM,
  fetchSessionMessages
} from "../../api/LLMAPI";

import ChatHeader from "./components/ChatHeader";
import ChatContainer from "./components/ChatContainer";
import ChatInput from "./components/ChatInput";
import FAQSuggestions from "./components/FAQSuggestions";
import InitialChatLayout from "./components/InitialChatLayout";
import ChatHistorySide from "./components/ChatHistorySide";



const MOCK_MESSAGES = [
  {
    role: "assistant",
    content: "Olá! Tudo bem? 😊\n\nComo posso ajudar hoje?",
  },
  {
    role: "user",
    content: "Quero testar o layout do chat.",
  },
  {
    role: "assistant",
    content:
      "Perfeito! 🚀\n\nAqui você consegue validar:\n- Alinhamento\n- Quebra de linha\n- Scroll\n- Estilo das mensagens",
  },
  {
    role: "user",
    content: "Ótimo, era isso mesmo!",
  },
];



const LLMPage = () => {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const location = useLocation();
  const [historyOpen, setHistoryOpen] = useState(false);

  /*useEffect(() => {
    // simula sessões vindas do backend
    const mockSessions = Array.from({ length: 12 }).map(
      (_, i) => `chat-${i + 1}`
    );

    setSessions(mockSessions);
    setSelectedSession(mockSessions[0]);
    setMessages(MOCK_MESSAGES);
  }, []);*/


  useEffect(() => {
    loadSessions();
  }, []);


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

      if (data?.length && !selectedSession) {
        const firstId =
          typeof data[0] === "string"
            ? data[0]
            : data[0].session_id;

        setSelectedSession(firstId);
      }
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

    setMessages((prev) => [
      ...prev,
      { role: "user", content: messageToSend },
    ]);

    try {
      const result = await sendMessageToLLM(messageToSend, selectedSession);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.message },
      ]);

    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "❌ Erro ao comunicar com a LLM." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  /*const handleCreateSession = () => {
    const newId = `chat-${sessions.length + 1}`;
    setSessions((prev) => [...prev, newId]);
    setSelectedSession(newId);
    setMessages([]);
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
      {
        role: "assistant",
        content: "Resposta mockada da LLM só para testar layout ✨",
      },
    ]);
  };*/


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

        <ChatHeader
          sessions={sessions}
          selectedSession={selectedSession}
          onSelectSession={setSelectedSession}
          onCreateSession={handleCreateSession}
          onToggleHistory={() => setHistoryOpen((prev) => !prev)}
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
              maxWidth: 900,
              height: "100%",
              overflowY: "auto",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {messages.length === 0 ? (
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
                  disabled={!selectedSession || loading}
                  loading={loading}
                />
                <FAQSuggestions
                  onSelectSuggestion={(text) => setInput(text)}
                />
              </Box>
            ) : (
              <>
                <ChatContainer messages={messages} />

                <Box sx={{ mt: "auto", }}>
                  <ChatInput
                    value={input}
                    onChange={setInput}
                    onSend={handleSend}
                    disabled={!selectedSession || loading}
                    loading={loading}
                  />
                </Box>
              </>
            )}
            </Box>
          </Box>
        </Box>
      </Box>
      {/* HISTÓRICO */}
    <ChatHistorySide
      open={historyOpen}
      onClose={() => setHistoryOpen(false)}
      sessions={sessions}
      selectedSession={selectedSession}
      onSelectSession={setSelectedSession}
      onCreateSession={handleCreateSession}
    />
  </Box>
);
};

export default LLMPage;
