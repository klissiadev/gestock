import { useEffect, useState, useRef } from "react";
import { fetchAllNotifications, markAsRead } from "../features/notifications/services/notificationApi";

export function useAllNotifications(limit = 20) {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState(null);

  const pendingReadRef = useRef(new Set());

  const cursor =
    notifications.length > 0
      ? notifications[notifications.length - 1].created_at
      : null;

  async function loadInitial() {
    try {
      setLoading(true);
      const data = await fetchAllNotifications(limit);
      setNotifications(data);
      setHasMore(data.length === limit);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadMore() {
    if (!hasMore || loading) return;

    try {
      setLoading(true);
      const data = await fetchAllNotifications(limit, cursor);
      setNotifications((prev) => [...prev, ...data]);
      setHasMore(data.length === limit);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // Marca localmente como lida
  function markAllAsReadLocally() {
    setNotifications((prev) =>
      prev.map((n) => {
        if (!n.read) {
          pendingReadRef.current.add(n.id);
        }
        return { ...n, read: true };
      })
    );
  }

  async function syncPendingReads() {
    const ids = Array.from(pendingReadRef.current);

    for (const id of ids) {
      try {
        await markAsRead(id);
      } catch (err) {
        console.error("Erro ao sincronizar notificação:", id);
      }
    }

    pendingReadRef.current.clear();
  }

  useEffect(() => {
    loadInitial();
  }, []);

  return {
    notifications,
    loading,
    error,
    hasMore,
    loadMore,
    markAllAsReadLocally,
    syncPendingReads,
  };
}