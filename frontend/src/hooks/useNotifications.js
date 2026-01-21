import { useEffect, useRef, useState } from "react";
// import { fetchUnreadNotifications } from "../features/notifications/services/notificationApi";
import { fetchUnreadNotifications } from "../features/notifications/services/notificationApi.mock";

export function useNotifications({
  limit = 5,
  pollingInterval = 30000, // 30s
} = {}) {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState(null);

  const pollingRef = useRef(null);

  // Cursor = created_at da última notificação
  const cursor =
    notifications.length > 0
      ? notifications[notifications.length - 1].created_at
      : null;


  async function loadInitial() {
    try {
      setLoading(true);
      const data = await fetchUnreadNotifications(limit);
      setNotifications(data);
      setHasMore(data.length === limit);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // paginação
  async function loadMore() {
    if (!hasMore || loading) return;

    try {
      setLoading(true);
      const data = await fetchUnreadNotifications(limit, cursor);
      setNotifications((prev) => [...prev, ...data]);
      setHasMore(data.length === limit);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // novas notificações
  async function pollNew() {
    try {
      const data = await fetchUnreadNotifications(limit);

      if (data.length === 0) return;

      setNotifications((prev) => {
        const existingIds = new Set(prev.map((n) => n.id));
        const fresh = data.filter((n) => !existingIds.has(n.id));
        return fresh.length ? [...fresh, ...prev] : prev;
      });
    } catch {
      // polling não deve quebrar a UI
    }
  }

  useEffect(() => {
    loadInitial();
    pollingRef.current = setInterval(pollNew, pollingInterval);
    return () => clearInterval(pollingRef.current);
  }, []);

  return {
    notifications,
    loading,
    error,
    hasMore,
    loadMore,
    reload: loadInitial,
  };
}
