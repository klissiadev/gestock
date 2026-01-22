import { NotificationItem } from "./NotificationItem";

export function NotificationList({ notifications = [] }) {
  if (!notifications.length) {
    return <p style={{ padding: 8 }}>Nenhuma notificação</p>;
  }

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 6 }}>
      {notifications.map((notification) => (
        <NotificationItem
          key={notification.id}
          notification={notification}
          onClick={() => console.log("clicou", notification.id)}
        />
      ))}
    </div>
  );
}
