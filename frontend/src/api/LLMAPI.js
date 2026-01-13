const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessageToLLM(message, sessionId = null, userId = null) {
  try {
    const response = await fetch(`${BASE_URL}/llm`, {
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
      console.error("Erro HTTP:", response.status, errorText);
      throw new Error("Erro HTTP ao chamar LLM");
    }

    return await response.json();
  } catch (error) {
    console.error("Erro no LLMAPI:", error);
    throw error;
  }
}