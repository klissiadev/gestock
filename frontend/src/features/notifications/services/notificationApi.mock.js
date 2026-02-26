// src/features/notifications/services/notificationApi.mock.js
import { notificationsMock } from "../../../features/notifications/mocks/notificationsMock";

export async function fetchUnreadNotifications(limit, cursor) {
  // simula delay de API
  await new Promise((res) => setTimeout(res, 300));

  let data = notificationsMock
    .filter((n) => !n.read)
    .sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at)
    );

  if (cursor) {
    data = data.filter(
      (n) => new Date(n.created_at) < new Date(cursor)
    );
  }

  return data.slice(0, limit);
}
