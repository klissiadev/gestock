import { InputBase, FormControl, Stack, Box } from "@mui/material";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import ArrowCircleUpRoundedIcon from "@mui/icons-material/ArrowCircleUpRounded";
import { useState, useEffect } from "react";

export const SearchBar = ({
  value,
  onChange,
  name = "searchTerm",
  placeholder = "Pesquisar...",
  debounce = 500,
}) => {
  const [displayValue, setDisplayValue] = useState(value || "");

  // Atualiza se o valor externo mudar
  useEffect(() => {
    setDisplayValue(value || "");
  }, [value]);

  // Debounce
  useEffect(() => {
    const handler = setTimeout(() => {
      onChange(name, displayValue);
    }, debounce);

    return () => clearTimeout(handler);
  }, [displayValue, name, onChange, debounce]);

  return (
    <FormControl
      fullWidth
      sx={{
        border: "1px solid",
        borderRadius: 3,
        borderColor: (theme) => theme.palette.common.black,
        padding: "2px 6px",
      }}
    >
      <Stack direction="row" alignItems="center" gap={2} p={0.5}>
        <SearchOutlinedIcon />

        <InputBase
          value={displayValue}
          onChange={(e) => setDisplayValue(e.target.value)}
          placeholder={placeholder}
          sx={{ flex: 1 }}
        />

        <Box display="flex" justifyContent="flex-end">
          <ArrowCircleUpRoundedIcon />
        </Box>
      </Stack>
    </FormControl>
  );
};

export default SearchBar;