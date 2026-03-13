const API_URL = "http://localhost:8000";

function getToken() {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("Usuário não autenticado");
  }

  return token;
}

export async function createRequest(payload) {
  const token = getToken();

  const response = await fetch(`${API_URL}/requisicoes/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("Erro backend:", data);
    throw new Error(data.detail || "Erro ao criar requisição");
  }

  return data;
}