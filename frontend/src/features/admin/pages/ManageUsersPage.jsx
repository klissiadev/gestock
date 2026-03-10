import React, { useCallback } from 'react'
import { Box, Stack, Avatar } from "@mui/material";
import TopBar from "../components/TopBar";
import CustomTable from '../components/CustomTable';
import { useEffect, useState } from "react";
import { useHeader } from "../../../HeaderContext";
import UserSvg from "../../../assets/icon/iconTeam.svg?react";

import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import EditSvg from "../../../assets/icon/iconEdit.svg?react";
import DeleteSvg from "../../../assets/icon/iconDelete.svg?react";

import { fetchUser } from '../services/fetchImportLogs';

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
    search_term: "",
    order_by: "",
    direction: "DESC"
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

  const columns = [
    {
      field: "nome",
      header: "Funcionário",
      render: (row) => (
        <Box display="flex" alignItems="center" gap={2} justifyContent="center">
          <Avatar
            sx={{
              width: 36,
              height: 36,
              backgroundColor: "#EAEAEA",
              color: "#555",
            }}
          >
            <PersonOutlineIcon fontSize="small" />
          </Avatar>
          {row.nome}
        </Box>
      ),
    },
    { field: "email", header: "Email" },
    { field: "funcao", header: "Função" },
  ];

  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const loadUsers = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchUser(filters);
      // Mapeia o campo "logs" do JSON para o nosso estado
      setUsers(data.logs || []);
      setTotal(data.total || 0);
    } catch (err) {
      console.error("Erro ao carregar usuários:", err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);


  const actions = [
    {
      icon: <EditSvg width={18} height={18} />,
      onClick: (row) => {
        console.log("Editar usuário:", row);
      },
    },
    {
      icon: <DeleteSvg width={18} height={18} />,
      onClick: (row) => {
        console.log("Excluir usuário:", row);
      },
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
        title="Usuários"
        icon={UserSvg}
        filters={filters}
        onFilterChange={handleFilterChange}
        orderOptions={orderOptions}
        searchPlaceholder="Buscar usuário..."
      />

      <CustomTable
        columns={columns}
        rows={users}
        actions={actions}
      />
    </Stack>
  )
}

export default UsersPage