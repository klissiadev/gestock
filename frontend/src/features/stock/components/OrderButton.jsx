import { useState } from "react";
import { Box, FormControl, IconButton } from "@mui/material";
import ArrowUpwardRoundedIcon from "@mui/icons-material/ArrowUpwardRounded";
import ArrowDownwardRoundedIcon from "@mui/icons-material/ArrowDownwardRounded";



const OrderButton = ({ radius = 2}) => {
  const [isAsc, setAsc] = useState(true);

  return (
    <FormControl fullWidth>
      <IconButton
        size="large"
        sx={{
          padding: 3,
          color: theme => theme.palette.common.black,
          borderStyle: "solid",
          borderWidth: "1px",
          borderRadius: radius
        }}
        onClick={() => setAsc(!isAsc)}
      >
        {isAsc ? (
          <ArrowUpwardRoundedIcon fontSize="inherit" />
        ) : (
          <ArrowDownwardRoundedIcon fontSize="inherit" />
        )}
      </IconButton>
    </FormControl>
  );
};

export default OrderButton;
