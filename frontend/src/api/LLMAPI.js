const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessageToLLM(message, sessionId = null, userId = null) {
  const response = await fetch(`${BASE_URL}/llm/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      user_id: userId,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Erro HTTP ${response.status}: ${errorText}`);
  }

  return await response.json();
}