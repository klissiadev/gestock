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
    <Box sx={{px: 4, py: 1, width: "100%", display: "flex", alignItems: "center", flexDirection: "column"}}>

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
          width: "60%",
        }}
      >
        <Box sx={{ flex: 1, overflowY: "auto" }}>
          {messages.length === 0 ? (
            <InitialChatLayout />
          ) : (
            <ChatContainer messages={messages} />
          )}
        </Box>
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
