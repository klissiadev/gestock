  const BASE_URL = "http://127.0.0.1:8000";

  export async function fetchSessions() {
    const response = await fetch(`${BASE_URL}/llm/sessions`);

    if (!response.ok) {
      throw new Error("Erro ao buscar sessões");
    }

    return await response.json();
  }

  export async function createSession() {
    const response = await fetch(`${BASE_URL}/llm/sessions`, {
      method: "POST",
    });

    if (!response.ok) {
      throw new Error("Erro ao criar sessão");
    }

    const data = await response.json();
    return data.session_id;
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

    const data = await response.json();

    return {
      message: data.response,
      sessionId: data.session_id
    };
  }


  export async function fetchSessionMessages(sessionId, limit = 100, offset = 0) {

    const response = await fetch(
      `${BASE_URL}/llm/sessions/${sessionId}/messages?limit=${limit}&offset=${offset}`
    );

    if (!response.ok) {
      throw new Error("Erro ao buscar histórico");
    }

    return response.json();
  }



  export async function streamMessageToLLM(message, sessionId, onChunk) {

  const response = await fetch(`${BASE_URL}/llm/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok || !response.body) {
    throw new Error("Erro ao enviar mensagem");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value, { stream: true });
    onChunk(chunk);
  }

}

