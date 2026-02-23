import { useEffect, useRef } from "react";
import { toast, Zoom } from "react-toastify";
import { useNotifications } from "../../../hooks/useNotifications";

export default function NotificationToast() {
  const { notifications } = useNotifications();

  // Guarda IDs já exibidos (anti-spam no front)
  const shownRef = useRef(new Set());

  useEffect(() => {
    notifications.forEach((notification) => {
      if (shownRef.current.has(notification.id)) return;

      toast(
      <div>
        <strong style={{ display: "block", marginBottom: 4 }}>
          {notification.title}
        </strong>
        <span>{notification.message}</span>
      </div>,
      {
        type: mapSeverity(notification.severity),
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: false,
        pauseOnHover: false,
        draggable: false,
        theme: "light",
        transition: Zoom,
      }
    );

      shownRef.current.add(notification.id);
    });
  }, [notifications]);

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
