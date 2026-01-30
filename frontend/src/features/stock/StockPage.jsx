import React from "react";
import { products } from "./mocks/productTable.mock";
import { PRODUCT_HEADER_NAMES } from "./constants/productConstant";
import { Divider, Stack } from "@mui/material";
import TableToolBar from "./components/TableToolBar";
import TableModel from "./components/tableModel";

const StockPage = () => {
  // Gerador de colunas (um dicionario com os campos: field e headerName)
  const columns = Object.keys(products[0]).map((key) => ({
    field: key,
    // Por enquanto: PRODUCT_HEADER_NAMES, mas devo encontrar uma forma de
    headerName:
      PRODUCT_HEADER_NAMES[key.toUpperCase()] ||
      key.replace("_", " ").toLowerCase(),
  }));

  const rows = products.map((p) => ({
    id: p.nome_produto,
    ...p,
  }));

  return (
    <Stack
      direction="column"
      spacing={2}
      sx={{
        backgroundColor: (theme) => theme.palette.common.white,
        width: "100%",
        padding: 1,
      }}
    >
      <TableToolBar />
      <Divider variant="middle" />
      <TableModel rows={rows} columns={columns} />
    </Stack>
  );
};

export default StockPage;
