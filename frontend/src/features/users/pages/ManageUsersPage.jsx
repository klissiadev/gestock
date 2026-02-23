import React from 'react'
import { Box, Stack } from "@mui/material";
import ManageUserBar from "../components/ManageUserBar";
import { useState } from 'react';

const UsersPage = () => {
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
      <ManageUserBar
        titulo={"Usuários"}
        filters={filters}
        onFilterChange={handleFilterChange}
      />
    </Stack>
  )
}

export default UsersPage