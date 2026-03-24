import React, { useState, useEffect } from "react";
import { Stack } from "@mui/material";
import TopBar from "../components/TopBar";
import ChatSvg from "../../../assets/icon/iconChat.svg?react";
import CustomTable from "../components/CustomTable";
import {  fetchChatLogs  } from "../services/fetchImportLogs";

const LogChatPage = () => {
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

      const response = await fetchChatLogs({
        direction,
        order_by: orderField,
        user_name: filters.searchTerm || null,
        period: null,
      });

      setRows(response.logs || []);
    } catch (error) {
      console.error("Erro ao buscar logs:", error.message);
    }
  };

  useEffect(() => {
    loadLogs();
  }, []);

  const orderOptions = [
    { value: "created_at_DESC", label: "Data (Mais recente)" },
    { value: "created_at_ASC", label: "Data (Mais antiga)" },
    { value: "user_id_ASC", label: "Usuário (A-Z)" },
    { value: "user_id_DESC", label: "Usuário (Z-A)" },
  ];

  const columns = [
    { field: "user_id", header: "Usuário ID" },
    { field: "session_id", header: "Sessão" },
    {
      field: "user_message",
      header: "Mensagem Usuário",
    },
    {
      field: "bot_response",
      header: "Resposta Bot",
    },
    {
      field: "created_at",
      header: "Data",
      render: (row) =>
        new Date(row.created_at).toLocaleString("pt-BR"),
    },
  ];

  return (
    <Stack
      direction="column"
      spacing={2}
      sx={{
        backgroundColor: (theme) => theme.palette.common.white,
        width: "100%",
        padding: 1,
        flex: 1,
      }}
    >
      <TopBar
        title="Log Conversas LLM"
        icon={ChatSvg}
        filters={filters}
        onFilterChange={handleFilterChange}
        orderOptions={orderOptions}
        searchPlaceholder="Buscar por usuário..."
      />

      <CustomTable columns={columns} rows={rows} />
    </Stack>
  );
};

export default LogChatPage;