import React, { useEffect } from "react";
import { products } from "./mocks/productTable.mock";
import { PRODUCT_HEADER_NAMES } from "./constants/productConstant";
import { Divider, Stack } from "@mui/material";
import TableToolBar from "./components/TableToolBar";
import TableModel from "./components/tableModel";
import { fetchProdutos } from "./services/produtctService";
import { useState } from "react";

const StockPage = () => {
  // Gerador de colunas mockados (um dicionario com os campos: field e headerName)
  const columns = Object.keys(PRODUCT_HEADER_NAMES).map((key) => ({
    field: key,
    headerName: PRODUCT_HEADER_NAMES[key],
  }));

  const rows = products.map((p) => ({
    id: p.nome_produto,
    ...p,
  }));

  const [filters, setFilters] = useState({
    searchTerm: "",
    orderBy: "",
    isAsc: true,
    categoria: "",
    isBaixoEstoque: false,
    isVencidos: false
  });

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

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
      <TableToolBar titulo={"Estoque"} filters={filters} onFilterChange={handleFilterChange}/>
      <Divider variant="middle" />
      <TableModel rows={rows} columns={columns} />
    </Stack>
  );
};

export default StockPage;
