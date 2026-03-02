const API_URL = "http://localhost:8000";

export async function fetchNotifications() {
  try {
    const token = localStorage.getItem("access_token");

    const response = await fetch(`${API_URL}/notificacoes`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`, // ← AQUI
      },
    });

    if (!response.ok) {
      throw new Error(`Erro na API: ${response.status}`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
      throw new Error("Formato inválido de notificações");
    }

    return data;
  } catch (error) {
    console.error("Erro ao buscar notificações:", error);
    return [];
  }
}

export async function fetchUnreadNotifications(limit = 5, cursor = null) {
  const token = localStorage.getItem("access_token");

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
        "Authorization": `Bearer ${token}`, // ← AQUI
      },
    }
  );

  if (!response.ok) {
    throw new Error("Erro ao buscar notificações");
  }

  return response.json();
}


export async function markAsRead(notificationId) {
  try {
    const token = localStorage.getItem("access_token");

    const response = await fetch(
      `${API_URL}/notificacoes/${notificationId}/read`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`, // ← AQUI
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Erro ao marcar como lida: ${response.status}`);
    }

    return true;
  } catch (error) {
    console.error("Erro ao marcar notificação como lida:", error);
    return false;
  }
}


