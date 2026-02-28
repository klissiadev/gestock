import React from "react";
import { Box, Typography, Stack } from "@mui/material";
import SearchBar from "./SearchBar";
import OrderSelector from "./OrderSelector";
import OrderButton from "./orderButton";
import DownloadButton from "./DownloadButton";

const TransactionToolBar = ({ titulo, filters, onFilterChange }) => {
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
            {titulo}
          </Typography>
        </Box>

        <Box sx={{ flex: 4, display: "flex", justifyContent: "center" }}>
          <Stack
            direction="row"
            spacing={2}
            alignItems="center"
            sx={{ width: "100%", justifyContent: "center" }}
          >
            <SearchBar value={filters.searchTerm} onChange={onFilterChange} placeholder="Buscar movimentação..." />
            <Stack
              direction="row"
              gap={1}
              sx={{ flexGrow: 1, maxWidth: 600, justifyContent: "center" }}
            >
              {/* Seletor de Ordenação */}
              <OrderSelector
                name="orderBy"
                value={filters.orderBy}
                onChange={onFilterChange}
                placeholder="Ordenar por..."
                startingPoint="unique_id"
                options={[
                  { value: "produto_nome", label: "Nome" },
                  { value: "tipo_movimento", label: "Tipo de Movimentação" },
                  { value: "created_at", label: "Data de criação" },
                ]}
              />
            </Stack>
          </Stack>
        </Box>

        <Box sx={{ flex: 1, display: "flex", justifyContent: "flex-end" }}>
          <Box sx={{ alignContent: "end" }}>
            <Stack direction={"row"} spacing={1} sx={{display: "flex", justifyContent: "center", alignItems: "center"}}>
              <DownloadButton filter={filters} whatTable={"transactions"} />
              <OrderButton
                radius={10}
                filter={filters.isAsc}
                onFilterChange={onFilterChange}
              />
            </Stack>
          </Box>
        </Box>
      </Stack>
    </div>
  );
};

export default TransactionToolBar;
