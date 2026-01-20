import { useEffect, useState, useCallback, useMemo } from "react";
import {
  fetchNotifications,
  markAsRead,
} from "../features/notifications/services/notificationApi";

export function useNotifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // fetch inicial

  const loadNotifications = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchNotifications();
      setNotifications(data);
    } catch (err) {
      console.error("Erro ao buscar notificações:", err);
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadNotifications();
  }, [loadNotifications]);

  const markNotificationAsRead = useCallback(async (id) => {
    try {
      await markAsRead(id);

      setNotifications((prev) =>
        prev.map((n) =>
          n.id === id
            ? { ...n, read_at: new Date().toISOString() }
            : n
        )
      );
    } catch (err) {
      console.error("Erro ao marcar notificação como lida:", err);
    }
  }, []);

  const unread = useMemo(
    () => notifications.filter((n) => !n.read_at),
    [notifications]
  );

  const unreadCount = unread.length;

  return {
    notifications,
    unread,
    unreadCount,
    loading,
    error,
    reload: loadNotifications,
    markAsRead: markNotificationAsRead,
  };
}
