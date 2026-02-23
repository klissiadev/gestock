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
      //setMessages([]);
      setTitle("Nova Conversa");
      return sessionId;
    } catch (err) {
      console.error("Erro ao criar sessão:", err);
    }
  };

  // Carrega as mensagens de uma sessão específica
  const loadMessages = useCallback(async (sid, isManual = false) => {
    if (!sid) return;
    try {
      const history = await llmAPI.fetchMessages(sid);

      // 💡 SÓ limpamos a tela se for um clique manual no histórico lateral
      if (isManual) setMessages([]);

      // 💡 A TRAVA DE SEGURANÇA:
      // Só atualizamos o estado se o banco de dados tiver mensagens.
      // Se o histórico vier vazio (o que acontece na primeira mensagem),
      // nós NÃO fazemos nada. Isso mantém a sua mensagem otimista na tela!
      if (history && history.length > 0) {
        setMessages(history.map(msg => ({
          id: msg.id || crypto.randomUUID(),
          role: msg.role,
          content: msg.content
        })));
      }

      const sessionTitle = await llmAPI.fetchTitle(sid);
      setTitle(sessionTitle || "Nova Conversa");
    } catch (err) {
      console.error("Erro ao carregar mensagens:", err);
    }
  }, []);

  // Ao mudar de sessão pelo histórico lateral, carregamos as mensagens daquela sessão
  const handleSessionChange = async (sid) => {
    setLoading(true);
    try {
      setSelectedSession(sid);
      setMessages([]); 
      await loadMessages(sid, true);
    } catch (error) {
      console.error("Erro ao mudar de sessão:", error);
    } finally {
      setLoading(false);
    }
  }

  // Fluxo de envio de mensagem
  const sendMessage = async (input) => {
    if (!input.trim()) return;

    setLoading(true);

    const assistantId = crypto.randomUUID();
    setMessages(prev => [
      ...prev,
      { role: "user", content: input },
      { id: assistantId, role: "assistant", content: "" }
    ]);

    // Criar nova sessão se nao tiver
    let currentId = selectedSession;
    if (!currentId) {
      currentId = await createNewSession();
    }

    try {
      let fullText = "";
      await llmAPI.streamMessage(input, currentId, (chunk) => {
        fullText += chunk;
        setMessages(prev => prev.map(msg =>
          msg.id === assistantId ? { ...msg, content: fullText } : msg
        ));
      });

      // Se for uma conversa nova, avisa para atualizar o título na lateral
      setUpdateTrigger(prev => !prev);
      setTimeout(async () => {
        await loadSessions();
        setUpdateTrigger(prev => !prev);
      }, 1500);

    } finally {
      setLoading(false);
    }
  };

  // Botao "enviar mensagem"
  const handleSend = async (manualText = null) => {

    const messageToSend = (typeof manualText === 'string') ? manualText : input;
    if (!messageToSend || !messageToSend.trim() || loading) return;
    setInput("");

    await sendMessage(messageToSend);
  };


  return {
    sessions, selectedSession, setSelectedSession,
    messages, setMessages, setTitle, loading, setLoading, title, updateTrigger,
    loadSessions, createNewSession, loadMessages, sendMessage, handleSessionChange,
    handleSend, input, setInput
  };

}