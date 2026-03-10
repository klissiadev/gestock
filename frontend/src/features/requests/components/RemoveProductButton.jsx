import { IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

const RemoveProductButton = ({ onClick }) => {
  return (
    <IconButton
      onClick={onClick}
      sx={{
        width: 24,
        height: 24,
        borderRadius: "50%",
        bgcolor: "#e9e9e9",
        color: "#9e9e9e",

        "&:hover": {
          bgcolor: "#e0e0e0"
        }
      }}
    >
      <CloseIcon sx={{ fontSize: 12 }} />
    </IconButton>
  );
};

export default RemoveProductButton;