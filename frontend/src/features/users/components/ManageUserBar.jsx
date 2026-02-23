import React from 'react'
import { Box, Typography, Stack, Divider} from "@mui/material";
import ExpandableIconButton from "../../../components/ui/ExpandableIconButton.jsx";
import OrderSelector from "../../stock/components/OrderSelector.jsx";
import SearchBar from './SearchBar.jsx';
import ChatSvg from "../../../assets/icon/iconChat.svg?react";
import UserSvg from "../../../assets/icon/iconTeam.svg?react";

const ManageUserBar = ({ titulo, filters, onFilterChange }) => {
    const orderOptions = [
        { value: "name_asc", label: "Nome (A-Z)" },
        { value: "name_desc", label: "Nome (Z-A)" },
    ];
  return (
    <Stack x={1}>
      <Stack direction="row" alignItems="center" pb={1}>
        <Box sx={{ flex: 1 }} />

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 2,
          }}
        >
          <UserSvg width={24} height={24} />
          <Typography fontSize={20} fontWeight={500}>
            {titulo}
          </Typography>
        </Box>

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <ExpandableIconButton
            icon={<ChatSvg width={16} height={16} />}
            origin="users"
            initialMessage="Olá Minerva, me ajude com o gerenciamento de usuários."
          />
        </Box>
      </Stack>
      <Divider variant="middle" />  
      <Stack direction="row" alignItems="center" mt={1}>
        {/* Esquerda */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-start",
            gap: 1,
          }}
        >
            <OrderSelector
                name="order"
                value={filters.order}
                onChange={onFilterChange}
                options={orderOptions}
                placeholder="Ordenar por"
                startingPoint=""
            />
        </Box>

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <SearchBar
            value={filters.searchTerm}
            onChange={onFilterChange}
            name="searchTerm"
            placeholder="Buscar usuário..."
          />
        </Box>

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-end"
          }}
        >  
        </Box>
      </Stack>
    </Stack>
  )
}

export default ManageUserBar