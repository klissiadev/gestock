import { useEffect, useState } from "react";
import { Box} from "@mui/material";
import { useLocation } from "react-router-dom";
import { useChatSession } from "../../ChatSessionContext";
import { useRef } from "react";

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
  const { getSession, setSession } = useChatSession();
  const initRef = useRef(false);
  const isBootstrappingRef = useRef(false);


  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    const initFromOrigin = async () => {
      const { chatOrigin, initialMessage } = location.state || {};
      if (!chatOrigin) return;

      isBootstrappingRef.current = true;

      let sessionId = getSession(chatOrigin);

      if (!sessionId) {
        sessionId = await createSession();
        setSession(chatOrigin, sessionId);
      }

      setSelectedSession(sessionId);

      if (initialMessage) {
        await sendInitialMessage(initialMessage, sessionId);
      }

      isBootstrappingRef.current = false;

      window.history.replaceState({}, document.title);
    };

    initFromOrigin();
  }, [location.state]);

  useEffect(() => {
    const loadMessages = async () => {
      if (!selectedSession) return;
      if (isBootstrappingRef.current) return;

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
      const sessionId = await createSession();

      setSelectedSession(sessionId); // primeiro

      await loadSessions(); // depois
    } catch (err) {
      console.error("Erro ao criar sessão:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !selectedSession) return;

    const messageToSend = input; // c ongela aqui

    setLoading(true);
    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", content: messageToSend },
    ]);

    try {
      const result = await sendMessageToLLM(messageToSend, selectedSession);

      setSelectedSession(result.sessionId);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.message },
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

  const sendInitialMessage = async (text, sessionId) => {
    setMessages([{ role: "user", content: text }]);

    const result = await sendMessageToLLM(text, sessionId);

    setSelectedSession(result.sessionId);

    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: result.message },
    ]);

    await loadSessions(); // 👈 importante
  };



  return (
    <Box
      sx={{
        height: "80vh",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        width: "100%",
        p: 1,
      }}
    >
      <ChatHeader
        sessions={sessions}
        selectedSession={selectedSession}
        onSelectSession={(id) => {
          setSelectedSession(id);
          
        }}
        onCreateSession={handleCreateSession}
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
);


};

export default LLMPage;
