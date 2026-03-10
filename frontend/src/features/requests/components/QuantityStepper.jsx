import { Box, IconButton, Typography } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";

const QuantityStepper = ({ value = 1, onIncrease, onDecrease }) => {
  return (
    <Box
      sx={(theme) => ({
        display: "flex",
        alignItems: "center",
        borderRadius: "6px",
        overflow: "hidden",
        height: 24,
        backgroundColor: theme.palette.iconButton.active,
      })}
    >
      <IconButton
        onClick={onDecrease}
        sx={{ color: "white", width: 24 }}
      >
        <RemoveIcon sx={{ fontSize: 16 }} />
      </IconButton>

      <Box
        sx={{
          width: 30,
          height: "100%",
          bgcolor: "white",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          p:1
        }}
      >
        <Typography fontSize={14} fontWeight={500}>
          {value}
        </Typography>
      </Box>

      <IconButton
        onClick={onIncrease}
        sx={{ color: "white", width: 24 }}
      >
        <AddIcon sx={{ fontSize: 16 }} />
      </IconButton>
    </Box>
  );
};

export default QuantityStepper;