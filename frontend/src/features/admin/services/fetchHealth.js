const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

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
      throw new Error("Sessão expirada. Faça login novamente.");
    }
    
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Erro na API: ${response.statusText}`);
  }

  return await response.json();
}


export const fetchHealth = async () => {
  try {
    const dados = await apiFetch("/admin/health");
    return dados;
  } catch (error) {
    console.error("Erro no Health Check:", error.message);
    throw new Error("Não foi possível buscar informações de saúde do sistema.");
  }
};

export const fetchHardware = async () => {
  try {
    const dados = await apiFetch("/admin/hardware");
    return dados;
  } catch (error) {
    console.error("Erro no Hardware Check:", error.message);
    throw new Error("Não foi possível buscar informações de hardware.");
  }
};