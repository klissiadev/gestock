import React from "react";
import { products } from "./mocks/productTable.mock";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableFooter,
} from "@mui/material";
import { Paper, Stack } from "@mui/material";

// TO DO: Criar o CSS desse datagrid de tal forma que é a tabela padrão

/* 
    Map -> percorre em todos os itens do array
    a cada item P => ele vai criar um novo objeto em que

    id = nome do produto
    ...p => copia todos os outros campos
    */

const StockPage = () => {
  // Gerador de colunas (um dicionario com os campos: field e headerName)
  const columns = Object.keys(products[0]).map((key) => ({
    field: key,
    headerName: key.replace("_", " ").toLowerCase(),
    flex: 1,
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
        backgroundColor: "white",
        width: "100%",
        padding: 10,
      }}
    >
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={col.field}>{col.headerName}</TableCell>
              ))}
            </TableRow>
          </TableHead>

          <TableBody>
            {rows.map((row) => (
              <TableRow
                key={row.id}
                hover
                sx={{
                  "&:hover td": {
                    backgroundColor: (theme) => theme.palette.table.hover,
                  },
                }}
              >
                {columns.map((col) => (
                  <TableCell
                    key={col.field}
                  >
                    {row[col.field]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>

          <TableFooter>

          </TableFooter>
        </Table>
      </TableContainer>
    </Stack>
  );
};

export default StockPage;
