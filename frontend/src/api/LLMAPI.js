const BASE_URL = "http://127.0.0.1:8000";

const getHeaders = (token) => ({
  "Content-Type": "application/json",
  "Authorization": `Bearer ${token}`
});

// Fetch autenticado principal
async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  const headers = {
    "Content-Type": "application/json",
    ...(token && { "Authorization": `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = "/";

      throw new Error("Sessão expirada");
    }
    throw new Error(`Erro na API: ${response.statusText}`);
  }
  return response;
};


export const llmAPI = {
  fetchSessions: () => apiFetch("/llm/sessions").then(r => r.json()),

  createSession: () => apiFetch("/llm/sessions", { method: "POST" }).then(r => r.json()),

  fetchMessages: (sid) => apiFetch(`/llm/sessions/${sid}/messages`).then(r => r.json()),

  fetchTitle: (sid) => apiFetch(`/llm/sessions/${sid}/title`).then(r => r.json()),

  // O stream continua especial por causa do reader
  streamMessage: async (message, session_id, onChunk) => {
    const response = await apiFetch("/llm/chat/stream", {
      method: "POST",
      body: JSON.stringify({ message, session_id }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      onChunk(decoder.decode(value, { stream: true }));
    }
  }
};






export async function fetchSessions(token) {
  const response = await fetch(`${BASE_URL}/llm/sessions`, {
    method: 'GET',
    headers: getHeaders(token),
  });

  if (!response.ok) throw new Error("Erro ao buscar sessões");
  return await response.json();
}

export async function createSession(token) {
  const response = await fetch(`${BASE_URL}/llm/sessions`, {
    method: "POST",
    headers: getHeaders(token),
  });

  if (!response.ok) throw new Error("Erro ao criar sessão");

  const data = await response.json();
  return data.session_id;
}

export async function sendMessageToLLM(message, sessionId, token) {
  const response = await fetch(`${BASE_URL}/llm/chat`, {
    method: "POST",
    headers: getHeaders(token),
    body: JSON.stringify({
      message,
      session_id: sessionId,
    }),
  });

  if (!response.ok) throw new Error("Erro ao enviar mensagem");

  const data = await response.json();
  return {
    message: data.response,
    sessionId: data.session_id
  };
}

export async function fetchSessionMessages(sessionId, token, limit = 100, offset = 0) {
  const response = await fetch(
    `${BASE_URL}/llm/sessions/${sessionId}/messages?limit=${limit}&offset=${offset}`,
    {
      method: 'GET',
      headers: getHeaders(token)
    }
  );

  if (!response.ok) throw new Error("Erro ao buscar histórico");
  return response.json();
}

export async function streamMessageToLLM(message, sessionId, token, onChunk) {
  const response = await fetch(`${BASE_URL}/llm/chat/stream`, {
    method: "POST",
    headers: getHeaders(token),
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok || !response.body) throw new Error("Erro ao enviar mensagem");

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value, { stream: true });
    onChunk(chunk);
  }
}