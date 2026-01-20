import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Select,
  MenuItem,
  TextField,
  Typography,
  Paper,
  CircularProgress,
} from "@mui/material";

import {
  fetchSessions,
  createSession,
  sendMessageToLLM,
} from "../../../api/LLMAPI";

const LLMPage = () => {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingSessions, setLoadingSessions] = useState(false);

  // Load sessions
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

  // Create session
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

  // Send message
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
    <Box sx={{ p: 3, maxWidth: 900, mx: "auto" }}>
      <Typography variant="h5" gutterBottom>
        Chat LLM (modo teste)
      </Typography>

      {/* Sessões */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Box display="flex" gap={2} alignItems="center">
          <Select
            fullWidth
            value={selectedSession}
            displayEmpty
            onChange={(e) => {
              setSelectedSession(e.target.value);
              setMessages([]);
            }}
          >
            <MenuItem value="">
              <em>Selecione uma sessão</em>
            </MenuItem>

            {sessions.map((s) => {
              const sessionId =
                typeof s === "string" ? s : s.session_id;

              return (
                <MenuItem key={sessionId} value={sessionId}>
                  {sessionId}
                </MenuItem>
              );
            })}
          </Select>

          <Button
            variant="contained"
            onClick={handleCreateSession}
            disabled={loading}
          >
            {loading ? <CircularProgress size={20} /> : "Nova sessão"}
          </Button>
        </Box>
      </Paper>

      {/* Chat */}
      <Paper
        sx={{
          p: 2,
          mb: 2,
          minHeight: 300,
          maxHeight: 400,
          overflowY: "auto",
        }}
      >
        {messages.length === 0 && (
          <Typography color="text.secondary">
            Nenhuma mensagem ainda.
          </Typography>
        )}

        {messages.map((msg, idx) => (
          <Typography
            key={idx}
            sx={{
              mb: 1,
              fontWeight: msg.role === "user" ? 600 : 400,
            }}
          >
            {msg.role === "user" ? "Você: " : "LLM: "}
            {msg.content}
          </Typography>
        ))}
      </Paper>

      {/* Input */}
      <Paper sx={{ p: 2 }}>
        <Box display="flex" gap={2}>
          <TextField
            fullWidth
            multiline
            minRows={2}
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder={
              selectedSession
                ? "Digite sua pergunta..."
                : "Selecione ou crie uma sessão"
            }
            disabled={!selectedSession || loading}
          />

          <Button
            variant="contained"
            onClick={handleSend}
            disabled={!selectedSession || loading}
          >
            {loading ? <CircularProgress size={20} /> : "Enviar"}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default LLMPage;
