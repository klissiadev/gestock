import { useState } from "react";
import { Select, FormControl, MenuItem } from "@mui/material";
import { theme } from "../../../style/theme";

const orderSelector = {
  backgroundColor: (theme) => theme.palette.button.main,
  borderStyle: "solid",
  borderWidth: "2px",
  borderRadius: 4,
  borderColor: (theme) => theme.palette.button.main,
  "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
    borderWidth: 0,
  },
};

const menuItem = {
  fontFamily: (theme) => theme.typography.fontFamily,
  "&:hover": {
    backgroundColor: (theme) => theme.palette.button.main,
  },
  "&.Mui-selected": {
    backgroundColor: (theme) => theme.palette.button.main,
  },
  "&.Mui-selected:hover": {
    backgroundColor: (theme) => theme.palette.button.main,
  },
  "&:focus": {
    backgroundColor: (theme) => theme.palette.button.main,
  },
};

const OrderSelector = ({ value, onChange, name, options, placeholder, startingPoint = "" }) => {


  return (
    <FormControl fullWidth>
      <Select
        value={value}
        displayEmpty
        onChange={(e) => onChange(name, e.target.value)}
        sx={orderSelector}
      >
        <MenuItem sx={menuItem} value={startingPoint}>
          {placeholder}
        </MenuItem>
        {options.map((opt) => (
          <MenuItem key={opt.value} sx={menuItem} value={opt.value}>
            {opt.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default OrderSelector;
