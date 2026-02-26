import React from 'react'
import { Box, Stack } from "@mui/material";
import TopBar from "../components/TopBar";
import TableUser from '../components/TableUser';
import { useEffect, useState } from "react";
import { useHeader } from "../../../HeaderContext";
import UserSvg from "../../../assets/icon/iconTeam.svg?react";

const UsersPage = () => {
  const { setHeaderConfig } = useHeader();

  useEffect(() => {
    setHeaderConfig((prev) => ({
      ...prev,
      variant: "users",
    }));

    return () => {
      setHeaderConfig((prev) => ({
        ...prev,
        variant: "default",
      }));
    };
  }, [setHeaderConfig]);

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

  const rows = [
    {
      id: 1,
      nome: "Nome Sobrenome",
      email: "nome_sobrenome@gmail.com",
      funcao: "Administrador",
    },
    {
      id: 2,
      nome: "Nome Sobrenome",
      email: "nome_sobrenome@gmail.com",
      funcao: "Técnico de Manutenção",
    },
  ];


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
        title="Usuários"
        icon={UserSvg}
        filters={filters}
        onFilterChange={handleFilterChange}
        orderOptions={orderOptions}
        searchPlaceholder="Buscar usuário..."
      />
      <TableUser rows={rows} selectedId={1} />

    </Stack>
  )
}

export default UsersPage