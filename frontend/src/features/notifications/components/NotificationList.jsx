import { useState } from "react";
import { NotificationItem } from "./NotificationItem";

export function NotificationList({ notifications, pageSize = 5 }) {
  const [page, setPage] = useState(1);

  const start = (page - 1) * pageSize;
  const end = start + pageSize;

  const totalPages = Math.ceil(notifications.length / pageSize);
  const currentItems = notifications.slice(start, end);

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 6 }}>
      {currentItems.map((notification) => (
        <NotificationItem
          key={notification.id}
          notification={notification}
          onClick={() => console.log("clicou", notification.id)}
        />
      ))}

      {/* Paginação */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          padding: "8px",
        }}
      >
        <button
          disabled={page === 1}
          onClick={() => setPage((p) => p - 1)}
        >
          Anterior
        </button>

        <span>
          Página {page} de {totalPages}
        </span>

        <button
          disabled={page === totalPages}
          onClick={() => setPage((p) => p + 1)}
        >
          Próxima
        </button>
      </div>
    </div>
  );
}
