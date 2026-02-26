import React from 'react'
import {Stack } from "@mui/material";
import TopBar from "../components/TopBar";
import { useState } from "react";
import ArchiveIcon from '@mui/icons-material/Archive';

const LogImportPage = () => {
  const [filters, setFilters] = useState({
    searchTerm: "",
    order: "",
  });

  const handleFilterChange = (name, value) => {
    setFilters((prev) => ({
    ...prev,
    [name]: value,
    }));

    console.log("Filtro alterado:", name, value);
  };

  const orderOptions = [
    { value: "name_asc", label: "Nome (A-Z)" },
    { value: "name_desc", label: "Nome (Z-A)" },
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

    </Stack>
  )
}

export default LogImportPage
