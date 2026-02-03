import React from "react";
import { Box, Typography, Stack } from "@mui/material";
import SearchBar from "./SearchBar";
import OrderSelector from "./OrderSelector";
import OrderButton from "./orderButton";
import ExpandableIconButton from "../../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../../assets/icon/iconChat.svg?react";

const TableToolBar = ({ titulo, filters, onFilterChange }) => {
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
            <SearchBar value={filters.searchTerm} onChange={onFilterChange} />
            <Stack
              direction="row"
              gap={1}
              sx={{ flexGrow: 1, maxWidth: 600, justifyContent: "center" }}
            >
              {/* Seletor de Categoria (Tipo) */}
              <OrderSelector
                name="categoria"
                value={filters.categoria}
                onChange={onFilterChange}
                placeholder="Todas as Categorias"
                options={[
                  { value: "Matéria Prima", label: "Matéria Prima" },
                  { value: "Semi Acabado", label: "Semi Acabado" },
                  { value: "Produto Acabado", label: "Produto Acabado" },
                ]}
              />
              {/* Seletor de Ordenação */}
              <OrderSelector
                name="orderBy"
                value={filters.orderBy}
                onChange={onFilterChange}
                placeholder="Ordenar por..."
                startingPoint="id"
                options={[
                  { value: "nome", label: "Nome" },
                  { value: "estoque_atual", label: "Quantidade" },
                  { value: "data_validade", label: "Vencimento" },
                ]}
              />
            </Stack>
          </Stack>
        </Box>

        <Box sx={{ flex: 1, display: "flex", justifyContent: "flex-end" }}>
          <Stack spacing={1} direction="row">
            <OrderButton radius={10} filter={filters.isAsc} onFilterChange={onFilterChange}/>
            <ExpandableIconButton
              icon={<ChatSvg width={20} height={20} />} 
              origin="sheets"
              initialMessage="Olá Minerva, me ajude com o estoque."
            />
          </Stack>
        </Box>
      </Stack>
    </div>
  );
};

export default TableToolBar;
