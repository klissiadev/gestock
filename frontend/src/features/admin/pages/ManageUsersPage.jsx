import { Stack, Box, Chip } from "@mui/material";
import TopBar from "../components/TopBar";
import CustomTable from '../components/CustomTable';
import { useEffect, useState, useCallback } from "react";
import { useHeader } from "../../../HeaderContext";

import UserSvg from "../../../assets/icon/iconTeam.svg?react";
import DeleteSvg from "../../../assets/icon/iconDelete.svg?react";
import useDebounce from '../../../hooks/useDebounce';

import { fetchUser, deleteUser } from '../services/fetchImportLogs';
import UserCell from '../components/UserCell';

// --- CONFIGURAÇÕES ESTÁTICAS ---
const ORDER_OPTIONS = [
  { value: "nome_asc", label: "Nome (A-Z)" },
  { value: "nome_desc", label: "Nome (Z-A)" },
];

const COLUMNS = [
  {
    field: "nome",
    header: "Funcionário",
    render: (row) => (<UserCell nome={row.nome} />),
  },
  {
    field: "email",
    header: "Email",
    render: (row) => (
      <Box sx={{ color: 'text.secondary', fontSize: '0.875rem' }}>
        {row.email}
      </Box>
    )
  },
  {
    field: "papel",
    header: "Função",
    render: (row) => (
      <Chip
        label={row.papel}
        size="small"
        variant="outlined"
        sx={{ padding: 1 }}
      />
    )
  },
];

const UsersPage = () => {
  const { setHeaderConfig } = useHeader();

  // Estados
  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search_term: "",
    order_by: "",
    direction: "DESC"
  });

  console.log(filters);

  const debouncedSearch = useDebounce(filters.search_term, 500);

  // Sincronização do header
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

  // Sincronização dos usuarios
  const loadUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [col, dir] = filters.order_by.split("_");

      const data = await fetchUser({
        search_term: debouncedSearch,
        order_by: col || "created_at",
        direction: dir?.toUpperCase() || "DESC"
      });

      setUsers(data.logs || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError("Não foi possível carregar os usuários.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [debouncedSearch, filters.order_by, filters.direction]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);


  // Handlers
  const handleFilterChange = (name, value) => {
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleDelete = async (user) => {
    if (window.confirm(`Deseja realmente remover ${user.nome}?`)) {
      try {
        await deleteUser(user.id);
        loadUsers(); // Recarrega a lista após deletar
      } catch (err) {
        console.error("Erro ao deletar:", err);
      }
    }
  };

  const actions = [
    {
      icon: <DeleteSvg width={18} height={18} />,
      onClick: (row) => {
        console.log("Excluir usuário:", row);
        handleDelete(row);
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
        orderOptions={ORDER_OPTIONS}
        searchPlaceholder="Buscar usuário..."
      />

      <CustomTable
        columns={COLUMNS}
        rows={users}
        actions={actions}
        loading={loading}
      />
    </Stack>
  )
}

export default UsersPage