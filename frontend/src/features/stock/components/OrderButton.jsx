import { useState } from "react";
import { Box, FormControl, IconButton } from "@mui/material";
import ArrowUpwardRoundedIcon from "@mui/icons-material/ArrowUpwardRounded";
import ArrowDownwardRoundedIcon from "@mui/icons-material/ArrowDownwardRounded";



const OrderButton = ({ radius = 2, filter, onFilterChange }) => {
  return (
    <FormControl>
      <IconButton
        size="medium"
        sx={{
          color: theme => theme.palette.common.black,
          borderStyle: "solid",
          borderWidth: "1px",
          borderRadius: radius
        }}
        onClick={() => onFilterChange("isAsc", !filter)}
      >
        {filter ? (
          <ArrowUpwardRoundedIcon fontSize="inherit" />
        ) : (
          <ArrowDownwardRoundedIcon fontSize="inherit" />
        )}
      </IconButton>
    </FormControl>
  );
};

export default OrderButton;
