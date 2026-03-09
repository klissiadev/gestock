const BASE_URL = "http://127.0.0.1:8000";

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

export const fetchHealth = () => apiFetch("/admin/health").then(r => r.json());