import { useEffect, useState } from "react";
import { Box} from "@mui/material";

import {
  fetchSessions,
  createSession,
  sendMessageToLLM,
} from "../../api/LLMAPI";

import ChatHeader from "./components/ChatHeader";
import ChatContainer from "./components/ChatContainer";
import ChatInput from "./components/ChatInput";
import FAQSuggestions from "./components/FAQSuggestions";
import InitialChatLayout from "./components/InitialChatLayout";

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

  useEffect(() => {
    loadSessions();
  }, []);

  /*useEffect(() => {
    // testee 
    setSelectedSession("mock-session");
    setMessages(MOCK_MESSAGES);
  }, []);*/ 

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
    setLoading(true);
    try {
      const result = await createSession();
      const sessionId =
        typeof result === "string" ? result : result.session_id;

      await loadSessions();
      setSelectedSession(sessionId);
      setMessages([]);
    } catch (err) {
      console.error("Erro ao criar sessão:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !selectedSession) return;

    setLoading(true);
    setMessages((prev) => [
      ...prev,
      { role: "user", content: input },
    ]);
    setInput("");

    try {
      const result = await sendMessageToLLM(input, selectedSession);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.answer },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Erro ao comunicar com a LLM.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{px: 4, py: 1, width: "100%", display: "flex", alignItems: "center", flexDirection: "column", height: "100%"}}>

      <ChatHeader
        sessions={sessions}
        selectedSession={selectedSession}
        onSelectSession={(id) => {
        setSelectedSession(id);
        setMessages([]);
        }}
        onCreateSession={handleCreateSession}
      />

      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          flex: 1,
          overflow: "hidden",
          alignItems: "center",
        }}
      >
        {/* MENSAGENS */}
        <Box
          sx={{
            flex: 1,
            overflowY: "hidden",
            width: "100%",  
            alignItems: "center",
          }}
        >
          {messages.length === 0 ? (
            <InitialChatLayout />
          ) : (
            <ChatContainer messages={messages} />
          )}
        </Box>

        {/* INPUT */}
        <ChatInput
          value={input}
          onChange={setInput}
          onSend={handleSend}
          disabled={!selectedSession || loading}
          loading={loading}
          hasMessages={messages.length > 0}
        />
      </Box>

      {messages.length === 0 ? (
        <FAQSuggestions
          onSelectSuggestion={(text) => {
          setInput(text);
          }}
        />
      ) : null}

    </Box>
  );
};

export default LLMPage;
