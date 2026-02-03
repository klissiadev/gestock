import { Box, Typography } from "@mui/material";
import { useState } from "react";

export default function ExpandableIconButton({
  icon,
  label = "Minerva",
  onClick,
}) {
  const [hover, setHover] = useState(false);

  return (
    <Box
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onClick={onClick}
      sx={(theme) => ({
        height: 48,
        width: hover ? 160 : 48,
        backgroundColor: theme.palette.iconButton.active,
        borderRadius: "12px",
        display: "flex",
        alignItems: "center",
        cursor: "pointer",
        overflow: "hidden",
        transition: "width 250ms cubic-bezier(0.4, 0, 0.2, 1), background-color 150ms",
        "&:hover": {
          backgroundColor: theme.palette.iconButton.hover,
        },
      })}
    >
      {/* Ícone */}
      <Box
        sx={(theme) => ({
          minWidth: 48,
          height: 48,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: theme.palette.iconButton.active,
          borderRadius: "12px",
        })}
      >
        {icon}
      </Box>

      {/* Label que "entra" */}
      <Typography
        sx={{
          whiteSpace: "nowrap",
          opacity: hover ? 1 : 0,
          transform: hover ? "translateX(0)" : "translateX(-12px)",
          transition: "all 200ms ease",
          fontSize: 18,
          fontWeight: 500,
          marginLeft: 2,
        }}
      >
        {label}
      </Typography>
    </Box>
  );
}
