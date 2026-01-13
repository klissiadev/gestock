import { useState } from "react";
import { sendMessageToLLM } from "../../../api/LLMAPI";

const LLMPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const result = await sendMessageToLLM(input);

      const botMessage = {
        role: "assistant",
        content: result.response,
      };

      setMessages((prev) => [...prev, botMessage]);
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
    <div style={{ padding: 24 }}>
      <h2>Chat LLM</h2>

      <div style={{ minHeight: 300, border: "1px solid #ccc", padding: 12 }}>
        {messages.map((msg, idx) => (
          <p key={idx}>
            <strong>{msg.role === "user" ? "Você" : "LLM"}:</strong>{" "}
            {msg.content}
          </p>
        ))}
      </div>

      <div style={{ marginTop: 12 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Digite sua pergunta..."
          style={{ width: "80%" }}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>
    </div>
  );
};

export default LLMPage;
