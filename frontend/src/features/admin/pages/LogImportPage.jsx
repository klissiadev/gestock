import React, { useState, useEffect } from "react";
import { Stack } from "@mui/material";
import TopBar from "../components/TopBar";
import ArchiveIcon from "@mui/icons-material/Archive";
import CustomTable from "../components/CustomTable";
import { fetchImportLogs } from "../services/fetchImportLogs";

const LogImportPage = () => {
  const [filters, setFilters] = useState({
    searchTerm: "",
    order: "created_at",
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
      const response = await fetchImportLogs({
        direction: "DESC",
        order_by: filters.order,
        search_term: filters.searchTerm || null,
        status: null,
        periodo: null,
        apenas_erro: false,
      });

      // Já vem com id, então só setar
      setRows(response.logs);
    } catch (error) {
      console.error("Erro ao buscar logs:", error.message);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [filters]);

  const orderOptions = [
    { value: "created_at", label: "Data" },
    { value: "nome_arquivo", label: "Nome do Arquivo" },
    { value: "usuario", label: "Usuário" },
  ];

  const columns = [
    { field: "nome_arquivo", header: "Arquivo" },
    { field: "qntd_registros", header: "Qtd Registros" },
    { field: "status", header: "Status" },
    { field: "usuario", header: "Usuário" },
    { 
      field: "registrado_em", 
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

      <CustomTable
        columns={columns}
        rows={rows}
      />
    </Stack>
  );
};

export default LogImportPage;