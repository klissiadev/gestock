import { useEffect, useRef, useState } from "react";
import { fetchUnreadNotifications } from "../features/notifications/services/notificationApi";

export function useUnreadNotifications({
  limit = 5,
  pollingInterval = 30000,
} = {}) {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);
  const pollingRef = useRef(null);

  async function loadUnread() {
    try {
      const data = await fetchUnreadNotifications(limit);
      setNotifications(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function pollNew() {
    try {
      const data = await fetchUnreadNotifications(limit);

      setNotifications((prev) => {
        const existingIds = new Set(prev.map((n) => n.id));
        const fresh = data.filter((n) => !existingIds.has(n.id));
        return fresh.length ? [...fresh, ...prev] : prev;
      });
    } catch {
      // polling silencioso
    }
  }

  useEffect(() => {
    loadUnread();
    pollingRef.current = setInterval(pollNew, pollingInterval);
    return () => clearInterval(pollingRef.current);
  }, []);

  return {
    notifications,
    unreadCount: notifications.length,
    reload: loadUnread,
    error,
  };
}