import React from "react";
import { Box, Typography, Stack, Divider} from "@mui/material";
import SearchBar from "./SearchBar";
import OrderSelector from "./OrderSelector";
import OrderBySelect from "./OrderBySelect";
import ExpandableIconButton from "../../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../../assets/icon/iconChat.svg?react";

import InvetorySvg from "../../../assets/icon/iconInventory.svg?react";
import DownloadButton from "./DownloadButton.jsx";

const TableToolBar = ({ titulo}) => {
  return (
    <Stack x={1}>
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
          <Typography fontSize={20} fontWeight={500}>
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
            icon={<ChatSvg width={16} height={16} />}
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

          <OrderBySelect
            name="ordenar"
            orderBy={filters.orderBy}
            isAsc={filters.isAsc}
            onChange={onFilterChange}
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
          <DownloadButton filter={filters} whatTable={"products"}/> 
        </Box>
      </Stack>
    </Stack>
  );
};

export default TableToolBar;
