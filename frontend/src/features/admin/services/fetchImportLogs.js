const api_url = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const fetchImportLogs = async (filters) => {
  const token = localStorage.getItem("token"); 

  if (!token) {
    throw new Error("Usuário não autenticado");
  }

  const response = await fetch(`${api_url}/admin/logs/importacao`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(filters),
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar logs de importação");
  }

  return response.json();
};

export const fetchUser = async (filters) => {
  const token = localStorage.getItem("token"); 

  if (!token) {
    throw new Error("Usuário não autenticado");
  }

  const response = await fetch(`${api_url}/admin/logs/usuarios`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(filters),
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar logs de usuarios");
  }

  return response.json();

};

export const fetchChatLogs = async (filters) => {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("Usuário não autenticado");
  }

  const response = await fetch(`${api_url}/admin/logs/minerva`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(filters),
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar logs da LLM");
  }

  return response.json();
};