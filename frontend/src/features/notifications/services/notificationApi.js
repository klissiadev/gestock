const API_URL = "http://localhost:8000";

function getToken() {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("Usuário não autenticado");
  }

  return token;
}

async function handleResponse(response) {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Erro na requisição");
  }

  return response.json();
}

export async function fetchUnreadNotifications(limit = 5, cursor = null) {
  const token = getToken();

  const params = new URLSearchParams({
    read: "false",
    limit: String(limit),
  });

  if (cursor) {
    params.append("cursor", cursor);
  }

  const response = await fetch(
    `${API_URL}/notificacoes?${params.toString()}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return handleResponse(response);
}

export async function fetchAllNotifications(limit = 20, cursor = null) {
  const token = getToken();

  const params = new URLSearchParams({
    limit: String(limit),
  });

  if (cursor) {
    params.append("cursor", cursor);
  }

  const response = await fetch(
    `${API_URL}/notificacoes?${params.toString()}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return handleResponse(response);
}

export async function markAsRead(notificationId) {
  const token = getToken();

  const response = await fetch(
    `${API_URL}/notificacoes/${notificationId}/read`,
    {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Erro ao marcar notificação como lida");
  }

  return true;
}


