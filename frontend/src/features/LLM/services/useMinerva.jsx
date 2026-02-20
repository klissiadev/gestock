import { useState, useCallback } from "react";
import { llmAPI } from "../../../api/LLMAPI"

export const useMinerva = () => {
  const [input, setInput] = useState("");
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [title, setTitle] = useState("Minerva");
  const [updateTrigger, setUpdateTrigger] = useState(false);

  // Carrega as sessões do usuario
  const loadSessions = useCallback(async () => {
    try {
      const data = await llmAPI.fetchSessions();
      setSessions(data || []);
    } catch (err) {
      console.error("Erro ao carregar sessões:", err);
    }
  }, []);

  // Cria uma nova sessão e marca ela
  const createNewSession = async () => {
    try {
      const data = await llmAPI.createSession();
      const sessionId = data.session_id;
      await loadSessions();
      setSelectedSession(sessionId);
      setMessages([]);
      setTitle("Nova Conversa");
      return sessionId;
    } catch (err) {
      console.error("Erro ao criar sessão:", err);
    }
  };

  // Carrega as mensagens de uma sessão específica
  const loadMessages = useCallback(async (sid) => {
    if (!sid) return;

    try {
      const history = await llmAPI.fetchMessages(sid);
      setMessages(history.map(msg => ({
        id: crypto.randomUUID(),
        role: msg.role,
        content: msg.content
      })));

      // Busca o título atualizado
      const sessionTitle = await llmAPI.fetchTitle(sid);
      console.log("Titulo achado: ", sessionTitle);
      setTitle(sessionTitle || "Nova Conversa");
      console.log("Titulo definido: ", title);
    } catch (err) {
      console.error("Erro ao carregar mensagens:", err);
    }
  }, []);

  // Fluxo de envio de mensagem
  const sendMessage = async (input) => {
    if (!input.trim()) return;

    // Criar nova sessão se nao tiver
    let currentId = selectedSession;
    if (!currentId) {
      currentId = await createNewSession();
    }

    const assistantId = crypto.randomUUID();
    setMessages(prev => [
      ...prev,
      { role: "user", content: input },
      { id: assistantId, role: "assistant", content: "" }
    ]);

    setLoading(true);
    try {
      let fullText = "";
      await llmAPI.streamMessage(input, currentId, (chunk) => {
        fullText += chunk;
        setMessages(prev => prev.map(msg =>
          msg.id === assistantId ? { ...msg, content: fullText } : msg
        ));
      });

      // Se for uma conversa nova, avisa para atualizar o título na lateral
      if (title === "Minerva" || title === "Nova Conversa") {
        setUpdateTrigger(prev => !prev);
      }
    } finally {
      setLoading(false);
    }
  };

  // Botao "enviar mensagem"
  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const messageToSend = input;
    setInput("");

    await sendMessage(messageToSend);
  };


  return {
    sessions, selectedSession, setSelectedSession,
    messages, loading, title, updateTrigger,
    loadSessions, createNewSession, loadMessages, sendMessage,
    handleSend, input, setInput
  };

}