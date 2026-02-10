import { Select, FormControl, MenuItem } from "@mui/material";

const OrderSelector = ({
  value,
  onChange,
  name,
  options,
  placeholder,
  startingPoint = "",
}) => {
  return (
    <FormControl sx={{ minWidth: 140 }}>
      <Select
        value={value}
        displayEmpty
        size="small"
        onChange={(e) => onChange(name, e.target.value)}
          renderValue={(selected) => {
            if (!selected) {
              return <span style={{ color: "#9e9e9e" }}>{placeholder}</span>;
            }

            const found = options.find((o) => o.value === selected);
            return found ? found.label : selected;
          }}
        sx={{
          height: 36,
          borderRadius: "8px",
          backgroundColor: (theme) => theme.palette.background.paper,

          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: (theme) => theme.palette.divider,
          },

          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: (theme) => theme.palette.text.primary,
          },

          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: (theme) => theme.palette.text.primary,
            borderWidth: "1px",
          },

          "& .MuiSelect-select": {
            paddingY: "8px",
            paddingX: "12px",
            display: "flex",
            alignItems: "center",
          },
        }}
      >
        <MenuItem value={startingPoint} disabled>
          {placeholder}
        </MenuItem>

        {options.map((opt) => (
          <MenuItem key={opt.value} value={opt.value}>
            {opt.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default OrderSelector;
