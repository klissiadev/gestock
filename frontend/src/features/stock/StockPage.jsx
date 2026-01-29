import React from "react";
import { products } from "./mocks/productTable.mock";
import { SearchBar } from "./components/SearchBar";
import OrderSelector from "./components/OrderSelector";

import { PRODUCT_HEADER_NAMES } from "./constants/productConstant";

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableFooter,
  Checkbox,

} from "@mui/material";
import { Paper, Stack } from "@mui/material";
import { theme } from "../../style/theme";
import OrderButton from "./components/orderButton";


// TO DO: maneira de alterar o HEADERNAME de forma dinamica.

const stack = {
  backgroundColor: "white",
  width: "100%",
  // padding: 1,
}

const tableMain = {
  backgroundColor: theme => theme.palette.table.main,
  borderRadius: 6,
  overflow: 'hidden'

}

const tableHead = {
  textAlign: 'center',
  fontFamily: theme => theme.typography.fontFamily,
  fontWeight: theme => theme.typography.fontWeightBold,
  borderBottom: theme => `1px solid ${theme.palette.common.black}`,
  backgroundColor: theme => theme.palette.table.main,
  tableLayout: 'fixed'
}

const tableRow = {
  "&:hover": {
    backgroundColor: theme => theme.palette.table.hover,
  },
  "&:active": {
    backgroundColor: theme => theme.palette.background.default,
  }
}

const tableCell = {
  textAlign: 'center',
  fontFamily: theme => theme.typography.fontFamily,
  fontWeight: theme => theme.typography.fontWeightLight,
}



const StockPage = () => {
  // Gerador de colunas (um dicionario com os campos: field e headerName)
  const columns = Object.keys(products[0]).map((key) => ({
    field: key,
    // Por enquanto: PRODUCT_HEADER_NAMES, mas devo encontrar uma forma de 
    headerName: PRODUCT_HEADER_NAMES[key.toUpperCase()] || key.replace("_", " ").toLowerCase(),
  }));

  const rows = products.map((p) => ({
    id: p.nome_produto,
    ...p
  }));

  return (
    <Stack
      direction="column"
      spacing={2}
      component={Paper}
      sx={stack}
    >

      <Stack
        direction="row"
        spacing={2}
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          gap: 2,
          width: "100%",
        }}>
        <SearchBar />
        <OrderSelector />
        <OrderSelector />
        <OrderButton />
      </Stack>



      <TableContainer >
        <Table stickyHeader sx={tableMain}>
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell sx={tableHead} key={col.field}>{col.headerName}</TableCell>
              ))}
            </TableRow>
          </TableHead>

          <TableBody>
            {rows.map((row) => (
              <TableRow
                key={row.id}
                sx={tableRow}
              >
                {columns.map((col) => (
                  <TableCell
                    key={col.field}
                    sx={tableCell}
                  >
                    {col.field === "ativo" ? (
                      <Checkbox checked={row[col.field]} disabled />
                    ) : (
                      row[col.field]
                    )}
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


