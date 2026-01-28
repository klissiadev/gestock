import React from "react";
import { products } from "./mocks/productTable.mock";
import { DataGrid } from "@mui/x-data-grid/DataGrid";
import { Box, Pagination, Stack } from "@mui/material";
import { theme } from "../../style/theme";

// TO DO: Criar o CSS desse datagrid de tal forma que é a tabela padrão

const StockPage = () => {
  // Gerador de colunas (um dicionario com os campos: field e headerName)
  const columns = Object.keys(products[0]).map((key) => ({
    field: key,
    headerName: key.replace("_", " ").toLowerCase(),
    flex: 1,
    sortable: false,
  }));

  const rows = products.map((p) => ({
    id: p.nome_produto,
    ...p,
  }));

  /* 
    Map -> percorre em todos os itens do array
    a cada item P => ele vai criar um novo objeto em que

    id = nome do produto
    ...p => copia todos os outros campos
    */

  const [paginationModel, setPaginationModel] = React.useState({
    page: 0,
    pageSize: 6,
  });

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
      <DataGrid
        columns={columns}
        rows={rows}
        // Setup do sistema de paginacao externo
        pagination
        paginationMode="client"
        paginationModel={paginationModel}
        onPaginationModelChange={setPaginationModel}
        pageSizeOptions={[paginationModel.pageSize]}
        hideFooter // Esconder o footer de paginacao
        autoHeight
        disableColumnMenu
        disableColumnSorting
        disableColumnFilter
        disableRowSelectionOnClick
        getRowHeight={() => "auto"}
        sx={{
          // root
          backgroundColor: (theme) => theme.palette.table.main,
          padding: 1,
          fontFamily: (theme) => theme.typography.fontFamily,
          borderRadius: 5,
          
          // Bloco de coluna
          "& .MuiDataGrid-columnHeader": {
            backgroundColor: (theme) => theme.palette.table.main,
            justifyContent: "center",
          },

          "& .MuiDataGrid-columnHeaders": {
            borderBottom: "1px solid",
            borderColor: (theme) => theme.palette.table.hover,
          },

          // container do título
          "& .MuiDataGrid-columnHeaderTitleContainer": {
            justifyContent: "center",
            fontWeight: (theme) => theme.typography.fontWeightBold,
          },

          // Texto da coluna
          "& .MuiDataGrid-columnHeaderTitle": {
            textAlign: "center",
            width: "100%",
          },

          // CSS de cada celula
          "& .MuiDataGrid-cell": {
            textAlign: "center",
            alignContent: "center",
            wordBreak: "break-word",
            whiteSpace: "normal",
            lineHeight: "1.4",
            py: 1,
            fontWeight: (theme) => theme.typography.fontWeightRegular,
          },

          // Animacao de hover de uma linha toda
          "& .MuiDataGrid-row:hover": {
            backgroundColor: (theme) => theme.palette.table.hover,
            borderRadius: 10,
          },

          // Celula quando e apertadas
          "& .MuiDataGrid-cell:focus, & .MuiDataGrid-cell:focus-within, & .MuiDataGrid-columnHeader:focus, & .MuiDataGrid-columnHeader:focus-within":
            {
              outline: "none",
            },
        }}
      />

      <Box sx={{ display: "flex", justifyContent: "center" }}>
        <Pagination
          count={Math.ceil(rows.length / paginationModel.pageSize)}
          page={paginationModel.page + 1}
          onChange={(e, value) =>
            setPaginationModel((prev) => ({
              ...prev,
              page: value - 1,
            }))
          }
          color="secondary"
          variant="outlined"
          shape="rounded"
        />
      </Box>
    </Stack>
  );
};

export default StockPage;
