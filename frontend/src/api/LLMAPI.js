const BASE_URL = "http://127.0.0.1:8000";

export async function fetchSessions() {
  const response = await fetch(`${BASE_URL}/llm/sessions`);
  if (!response.ok) {
    throw new Error("Erro ao buscar sessões");
  }
  return response.json();
}

export async function createSession() {
  const response = await fetch(`${BASE_URL}/llm/sessions`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Erro ao criar sessão");
  }

  return response.json();
}

export async function sendMessageToLLM(message, sessionId) {
  const response = await fetch(`${BASE_URL}/llm/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error("Erro ao enviar mensagem");
  }

  return response.json();
}