import { useEffect, useRef } from "react";
import { toast } from "react-toastify";
import { useNotifications } from "../../../hooks/useNotifications";

export default function NotificationToastTester() {
  const { unread } = useNotifications();

  // Guarda IDs já exibidos (anti-spam no front)
  const shownRef = useRef(new Set());

  useEffect(() => {
    unread.forEach((notification) => {
      if (shownRef.current.has(notification.id)) return;

      toast(notification.message, {
        type: mapSeverity(notification.severity),
      });

      shownRef.current.add(notification.id);
    });
  }, [unread]);

  return null; 
}

function mapSeverity(severity) {
  switch (severity) {
    case "CRITICAL":
      return "error";
    case "WARNING":
      return "warning";
    case "SUCCESS":
      return "success";
    case "INFO":
    default:
      return "info";
  }
}
