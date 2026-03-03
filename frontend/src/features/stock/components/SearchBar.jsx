import { InputBase, FormControl, Stack, Box } from "@mui/material";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import { useState, useEffect } from "react";

export const SearchBar = ({
  value = "",
  onChange,
  name = "search",
  placeholder = "Buscar...",
  debounce = 500,
  endIcon = null,
  fullWidth = true,
}) => {
  const [displayValue, setDisplayValue] = useState(value);

  useEffect(() => {
    setDisplayValue(value);
  }, [value]);

  useEffect(() => {
    const handler = setTimeout(() => {
      if (onChange) {
        onChange(name, displayValue);
      }
    }, debounce);

    return () => clearTimeout(handler);
  }, [displayValue, debounce, name, onChange]);

  return (
    <FormControl
      fullWidth={fullWidth}
      sx={{
        border: "1px solid",
        borderRadius: 3,
        borderColor: (theme) => theme.palette.common.black,
        padding: "2px 6px",
      }}
    >
      <Stack
        direction="row"
        alignItems="center"
        gap={2}
        padding={0.4}
      >
        <SearchOutlinedIcon />

        <InputBase
          value={displayValue}
          onChange={(e) => setDisplayValue(e.target.value)}
          placeholder={placeholder}
          sx={{
            flex: 1,
            "::placeholder": {
              fontFamily: (theme) => theme.typography.fontFamily,
              fontWeight: (theme) => theme.typography.fontWeightLight,
            },
          }}
        />

        {endIcon && (
          <Box display="flex" justifyContent="flex-end">
            {endIcon}
          </Box>
        )}
      </Stack>
    </FormControl>
  );
};

export default SearchBar;