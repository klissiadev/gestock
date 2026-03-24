import { Box, IconButton, MenuItem, Select, Typography } from "@mui/material";
import CalendarSvg from '@mui/icons-material/CalendarToday';
const months = [
  { value: 1, label: "Jan" },
  { value: 2, label: "Fev" },
  { value: 3, label: "Mar" },
  { value: 4, label: "Abr" },
  { value: 5, label: "Mai" },
  { value: 6, label: "Jun" },
  { value: 7, label: "Jul" },
  { value: 8, label: "Ago" },
  { value: 9, label: "Set" },
  { value: 10, label: "Out" },
  { value: 11, label: "Nov" },
  { value: 12, label: "Dez" },
];

export default function PeriodSelector({ value, onChange }) {
  const { year, month } = value;

  function handleMonthChange(event) {
    onChange({ year, month: event.target.value });
  }

  function handleYearChange(event) {
    onChange({ year: event.target.value, month });
  }

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        boxShadow: "0 4px 20px rgba(0,0,0,0.16)",
        borderRadius: "14px",
        px: 2,
        py: 0.5,
        gap: 1,
        bgcolor: "background.paper",
        color:(theme)=> theme.palette.primary.main
      }}
    >
      <CalendarSvg sx={{color:(theme)=> theme.palette.primary.main, width:"16px"}}/>

      <Select
        value={month}
        onChange={handleMonthChange}
        variant="standard"
        disableUnderline
        sx={{
          fontSize: 14,
          minWidth: 55,
        }}
      >
        {months.map((m) => (
          <MenuItem key={m.value} value={m.value}>
            {m.label}
          </MenuItem>
        ))}
      </Select>

      <Typography fontSize={14}>/</Typography>

      <Select
        value={year}
        onChange={handleYearChange}
        variant="standard"
        disableUnderline
        sx={{
          fontSize: 14,
          minWidth: 65,
        }}
      >
        {[2024, 2025, 2026, 2027, 2028].map((y) => (
          <MenuItem key={y} value={y}>
            {y}
          </MenuItem>
        ))}
      </Select>
    </Box>
  );
}
