import { Divider, Stack } from "@mui/material";
import TableToolBar from "../components/TableToolBar";
import TableModel from "../components/tableModel";
import { useProductTable } from "../hooks/useProductTable";
import LoadingComponent from "../components/LoadingComponent";
import ErrorState from "../components/ErrorState";

const TabelaProduto = () => {
  const { rows, columns, loading, error, filters, handleFilterChange, resetFilters } =
    useProductTable();

  console.log(filters);

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
      <TableToolBar
        titulo={"Estoque"}
        filters={filters}
        onFilterChange={handleFilterChange}
      />

      <Divider variant="middle" />

      {loading ? (
        <LoadingComponent columns={columns} />
      ) : error ? (
        <ErrorState 
          message={error} 
          onRetry={() => handleFilterChange('searchTerm', filters.searchTerm)} 
        />
      ) : (
        <TableModel rows={rows} columns={columns} />
      )}
    </Stack>
  );
};

export default TabelaProduto;
