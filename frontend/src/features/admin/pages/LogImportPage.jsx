import React, { useState, useEffect } from "react";
import { Stack } from "@mui/material";
import TopBar from "../components/TopBar";
import ArchiveIcon from "@mui/icons-material/Archive";
import CustomTable from "../components/CustomTable";
import { fetchImportLogs } from "../services/fetchImportLogs";

const LogImportPage = () => {
  const [filters, setFilters] = useState({
    searchTerm: "",
    order: "created_at_DESC",
  });

  const [rows, setRows] = useState([]);

  const handleFilterChange = (name, value) => {
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const loadLogs = async () => {
    try {
      const lastUnderscoreIndex = filters.order.lastIndexOf("_");

      const orderField = filters.order.substring(0, lastUnderscoreIndex);
      const direction = filters.order.substring(lastUnderscoreIndex + 1);

      const response = await fetchImportLogs({
        direction,
        order_by: orderField,
        search_term: filters.searchTerm || null,
        status: null,
        periodo: null,
        apenas_erro: false,
      });

      setRows(response.logs);
    } catch (error) {
      console.error("Erro ao buscar logs:", error.message);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [filters]);

  const orderOptions = [
    { value: "created_at_DESC", label: "Data (Mais recente)" },
    { value: "created_at_ASC", label: "Data (Mais antiga)" },
    { value: "nome_arquivo_ASC", label: "Nome Arquivo(A-Z)" },
    { value: "nome_arquivo_DESC", label: "Nome Arquivo (Z-A)" },
    { value: "status_ASC", label: "Status (A-Z)" },
    { value: "status_DESC", label: "Status (Z-A)" },
  ];

  const columns = [
    { field: "nome_arquivo", header: "Arquivo" },
    { field: "qntd_registros", header: "Qtd Registros" },
    { field: "status", header: "Status" },
    { field: "user_id", header: "Usuário" },
    { 
      field: "created_at", 
      header: "Data",
      render: (row) =>
        new Date(row.created_at).toLocaleString("pt-BR")
    },
  ];

  return (
    <Stack
      direction="column"
      spacing={2}
      sx={{
        backgroundColor: (theme) => theme.palette.common.white,
        padding: 2,
        flex: 1,
        height: "100vh",
        width: "100%",
      }}
    >
      <TopBar
        title="Log Importações"
        icon={ArchiveIcon}
        filters={filters}
        onFilterChange={handleFilterChange}
        orderOptions={orderOptions}
        searchPlaceholder="Buscar Importação..."
      />

      <CustomTable columns={columns} rows={rows} />
    </Stack>
  );
};

export default LogImportPage;