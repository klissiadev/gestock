const API_URL = "http://localhost:8000";

function getToken() {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("Usuário não autenticado");
  }

  return token;
}

export async function fetchSuggestions() {
  const token = getToken();

  const response = await fetch(`${API_URL}/previsao/sugestoes-compra-insumos`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("Erro backend:", data);
    throw new Error(data.detail || "Erro ao buscar sugestões");
  }

  return (data || []).map((item) => ({
    id: item.materia_prima_id,
    name: item.nome_materia_prima,
    type: "Matéria prima",
    qty: item.quantidade_sugerida_compra,
    priority: true,
  }));
}