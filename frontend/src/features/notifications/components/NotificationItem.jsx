import { Box, Typography, Stack } from "@mui/material";
import FiberManualRecordIcon from "@mui/icons-material/FiberManualRecord";
import DoneIcon from "@mui/icons-material/Done";

export function NotificationItem({ data }) {
  const isUnread = !data.read;

  const severityStyle = getSeverityStyle(data.severity);

  return (
    <Box
      sx={{
        bgcolor: isUnread ? severityStyle.bgColor : "#eeeeee",
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
            <FiberManualRecordIcon
              fontSize="small"
              sx={{ color: severityStyle.dotColor }}
            />
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
            <Typography
              fontWeight={600}
              color={isUnread ? severityStyle.textColor : "inherit"}
            >
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

// Formatação data
function formatDate(date) {
  const d = new Date(date);

  return d.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getSeverityStyle(severity) {
  switch (severity) {
    case "error":
    case "warning":
    case "critical":
      return {
        dotColor: "#d32f2f",
        bgColor: "#ffebee",
        textColor: "#b71c1c",
      };

    case "success":
      return {
        dotColor: "#2e7d32",
        bgColor: "#e8f5e9",
        textColor: "#1b5e20",
      };

    default:
      return {
        dotColor: "#1976d2",
        bgColor: "#e3f2fd",
        textColor: "#0d47a1",
      };
  }
}