
import { Divider, Stack } from "@mui/material";
import TransactionToolBar from "../components/TransactionToolBar";
import TableModel from "../components/tableModel";
import LoadingComponent from "../components/LoadingComponent";
import ErrorState from "../components/ErrorState";
import { useMovimentTable } from '../hooks/useMovimentTable';


const TabelaMovimentacao = () => {
    const { rows, columns, loading, error, filters, handleFilterChange, resetFilters } = useMovimentTable();
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
      <TransactionToolBar
        titulo={"Movimentacao"}
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
    )
}

export default TabelaMovimentacao
