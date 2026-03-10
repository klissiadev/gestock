import {
  Box,
  Typography,
  CircularProgress,
  Button,
  Stack,
  Divider,
} from "@mui/material";
import { useAllNotifications } from "../../hooks/useAllNotifications";
import { NotificationItem } from "./components/NotificationItem";
import { useEffect, useRef } from "react";

export default function NotificationsPage() {
  const {
    notifications,
    loading,
    error,
    hasMore,
    loadMore,
    markAllAsReadLocally,
    syncPendingReads,
  } = useAllNotifications(10);


  const didMarkRef = useRef(false);
  useEffect(() => {
    if (!didMarkRef.current && notifications.length > 0) {
      markAllAsReadLocally();
      didMarkRef.current = true;
    }
  }, [notifications]);

  useEffect(() => {
    const handleBeforeUnload = () => {
      syncPendingReads();
    };

    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      syncPendingReads();
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, []);

  return (
    <Stack
      direction="column"
      spacing={2}
      sx={{
        backgroundColor: (theme) => theme.palette.common.white,
        padding: 2,
        flex: 1,
        height: "100vh",
        width: "100%",
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 2,
        }}
      >
        <Typography fontSize={20} fontWeight={500}>
          Notificações
        </Typography>
      </Box>

      <Divider variant="middle" />

      {/* Lista */}
      <Box
        sx={{
          flex: 1,
          pr: 1,
          pb:2
        }}
      >
        {notifications.map((notification) => (
          <NotificationItem key={notification.id} data={notification} />
        ))}

        {loading && (
          <Box textAlign="center" py={2}>
            <CircularProgress size={24} />
          </Box>
        )}

        {!loading && hasMore && (
          <Box textAlign="center" mt={2}>
            <Button onClick={loadMore}>
              Carregar mais
            </Button>
          </Box>
        )}

        {!loading && notifications.length === 0 && (
          <Typography align="center" mt={4} color="text.secondary">
            Nenhuma notificação encontrada
          </Typography>
        )}

        {error && (
          <Typography align="center" mt={2} color="error">
            {error}
          </Typography>
        )}
      </Box>
    </Stack>
  );
}