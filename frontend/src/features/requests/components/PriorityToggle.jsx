import { Box, Typography, Switch } from "@mui/material";

const PriorityToggle = ({ checked, onChange }) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Typography fontSize={10}>
        Prioridade
      </Typography>

      <Switch
        checked={checked}
        onChange={onChange}
      />
    </Box>
  );
};

export default PriorityToggle;