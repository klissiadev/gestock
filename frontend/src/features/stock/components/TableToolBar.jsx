import React from "react";
import { Box, Typography, Stack, Divider} from "@mui/material";
import SearchBar from "./SearchBar";
import OrderSelector from "./OrderSelector";
import OrderButton from "./orderButton";
import ExpandableIconButton from "../../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../../assets/icon/iconChat.svg?react";

import InvetorySvg from "../../../assets/icon/iconInventory.svg?react";

const TableToolBar = ({ titulo, filters, onFilterChange }) => {
  return (
    <Stack x={1} pt={1}>
      <Stack direction="row" alignItems="center" pb={1}>
        <Box sx={{ flex: 1 }} />

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 2,
          }}
        >
          <InvetorySvg width={26} height={26} />
          <Typography variant="h5">
            {titulo}
          </Typography>
        </Box>

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <ExpandableIconButton
            icon={<ChatSvg width={20} height={20} />}
            origin="sheets"
            initialMessage="Olá Minerva, me ajude com o estoque."
          />
        </Box>
      </Stack>
      <Divider variant="middle" />   
      <Stack direction="row" alignItems="center" mt={1}>
        {/* Esquerda */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-start",
            gap: 1,
          }}
        >
          <OrderSelector
            name="categoria"
            value={filters.categoria}
            onChange={onFilterChange}
            placeholder="Categorias"
            options={[
              { value: "Matéria Prima", label: "Matéria Prima" },
              { value: "Semi Acabado", label: "Semi Acabado" },
              { value: "Produto Acabado", label: "Produto Acabado" },
            ]}
          />

          <OrderSelector
            name="orderBy"
            value={filters.orderBy}
            onChange={onFilterChange}
            placeholder="Ordenar"
            startingPoint="id"
            options={[
              { value: "nome", label: "Nome" },
              { value: "estoque_atual", label: "Quantidade" },
              { value: "data_validade", label: "Vencimento" },
            ]}
          />
        </Box>

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <SearchBar
            value={filters.searchTerm}
            onChange={onFilterChange}
          />
        </Box>

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-end",
            gap: 1,
          }}
        >
          <OrderButton
            radius={10}
            filter={filters.isAsc}
            onFilterChange={onFilterChange}
          />
        </Box>
      </Stack>
    </Stack>
  );
};

export default TableToolBar;
