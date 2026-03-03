import { Box, Typography, Stack } from "@mui/material";
import FiberManualRecordIcon from "@mui/icons-material/FiberManualRecord";
import DoneIcon from "@mui/icons-material/Done";

export function NotificationItem({ data }) {
  const isUnread = !data.read;

  return (
    <Box
      sx={{
        bgcolor: isUnread ? "#ffffff" : "#eeeeee",
        borderRadius: 2,
        p: 2,
        mb: 2,
        transition: "0.2s",
        cursor: "pointer",
        "&:hover": {
          transform: "scale(1.01)",
        },
      }}
    >
      <Stack direction="row" spacing={2}>
        {/* Status Icon */}
        <Box mt={0.5}>
          {isUnread ? (
            <FiberManualRecordIcon fontSize="small" />
          ) : (
            <DoneIcon fontSize="small" />
          )}
        </Box>

        {/* Conteúdo */}
        <Box flex={1}>
          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
          >
            <Typography fontWeight={600}>
              {data.title}
            </Typography>

            <Typography variant="caption" color="text.secondary">
              {formatDate(data.created_at)}
            </Typography>
          </Stack>

          <Typography
            variant="body2"
            color="text.secondary"
            mt={0.5}
          >
            {data.message}
          </Typography>
        </Box>
      </Stack>
    </Box>
  );
}

// Formatação simples
function formatDate(date) {
  const d = new Date(date);
  return d.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "short",
  });
}