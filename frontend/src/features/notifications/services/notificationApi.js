// frontend/src/features/services/notificationApi.js

import axios from "@/lib/axios";
import { normalizeNotification } from "../services/notificationNormalizer";

export async function fetchNotifications() {
  const { data } = await axios.get("/notificacoes");

  return data
    .map(normalizeNotification)
    .filter(Boolean);
}

export async function markAsRead(notificationId) {
  await axios.patch(`/notificacoes/${notificationId}/read`);
}
