export function NotificationItem({ notification, onClick }) {
  const { title, message, read, createdAt } = notification;

  return (
    <div
      onClick={onClick}
      style={{
        padding: "12px",
        borderBottom: "1px solid #e5e7eb",
        cursor: "pointer",
        backgroundColor: read ? "#fff" : "#f0f9ff",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <strong>{title}</strong>

        {!read && (
          <span
            style={{
              width: 8,
              height: 8,
              backgroundColor: "#3b82f6",
              borderRadius: "50%",
            }}
          />
        )}
      </div>

      <p
        style={{
          margin: "6px 0",
          color: "#555",
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
          maxWidth: "100%",
        }}
      >
        {message}
      </p>

      <small style={{ color: "#888" }}>
        {new Date(createdAt).toLocaleString()}
      </small>
    </div>
  );
}
