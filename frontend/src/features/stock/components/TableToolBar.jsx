import React from "react";
import { Box, Typography, Stack } from '@mui/material';
import SearchBar from "./SearchBar";
import OrderSelector from "./OrderSelector";
import OrderButton from "./orderButton";

const TableToolBar = () => {
  return (
    <div>
      {/* Barra de personalizacao */}
      <Stack
        direction="row"
        alignItems="center"
        paddingLeft={2}
        paddingRight={2}
        paddingTop={2}
      >
        <Box sx={{ flex: 1, display: "flex", justifyContent: "flex-start" }}>
          <Typography
            variant="h6"
            sx={{
              fontFamily: (theme) => theme.typography.fontFamily,
              fontWeight: (theme) => theme.typography.fontWeightLight,
            }}
          >
            Estoque
          </Typography>
        </Box>

        <Box sx={{ flex: 4, display: "flex", justifyContent: "center" }}>
          <Stack
            direction="row"
            spacing={2} // Espaço entre os elementos internos (Busca e Selects)
            alignItems="center"
            sx={{ width: "100%", justifyContent: "center" }}
          >
            <SearchBar />
            {/* SearchBar ocupando espaço disponível, mas com limite */}
            <Stack
              direction="row"
              gap={1}
              sx={{ flexGrow: 1, maxWidth: 600, justifyContent: "center" }}
            >
              <OrderSelector />
              <OrderSelector />
            </Stack>
          </Stack>
        </Box>

        <Box sx={{ flex: 1, display: "flex", justifyContent: "flex-end" }}>
          <Box sx={{ alignContent: "end" }}>
            <OrderButton radius={10} />
          </Box>
        </Box>
      </Stack>
    </div>
  );
};

export default TableToolBar;
