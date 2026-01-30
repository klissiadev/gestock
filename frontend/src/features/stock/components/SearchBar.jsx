import { InputBase, FormControl, Stack, Box } from "@mui/material";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import ArrowCircleUpRoundedIcon from "@mui/icons-material/ArrowCircleUpRounded";

export const SearchBar = () => {
  const searchBarStyle = {
    borderStyle: "solid",
    borderWidth: "2px",
    borderRadius: 4,
    borderColor: (theme) => theme.palette.common.black,
    padding: "4px 8px",
    "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
      borderWidth: 0,
    },
  };

  const searchBarStack = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: 2,
    padding: 0.4,
  };

  const searchbutton = {
    color: (theme) => theme.palette.common.black,
  };

  return (
    <FormControl fullWidth sx={searchBarStyle}>
      <Stack direction={"row"} sx={searchBarStack}>
        <SearchOutlinedIcon />

        <InputBase
          id="search"
          placeholder="Procure produto ..."
          sx={{
            flex: 1,
            "::placeholder": {
              fontFamily: (theme) => theme.typography.fontFamily,
              fontWeight: (theme) => theme.typography.fontWeightLight,
            },
          }}
        />

        <Box sx={{ flex: 1, display: "flex", justifyContent: "flex-end" }}>
          <Box sx={{ alignContent: "end" }}>
            <ArrowCircleUpRoundedIcon />
          </Box>
        </Box>
      </Stack>
    </FormControl>
  );
};

export default SearchBar;
