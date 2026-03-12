import { Box, Typography, Divider } from "@mui/material";
import { useState, useMemo } from "react";

import SearchBar from "../../stock/components/SearchBar";
import PurchaseSuggestions from "./PurchaseSuggestions";
import SearchProductList from "./SearchProductList";

const RequestMainPanel = ({ suggestions, onSelectSuggestion }) => {
  const [search, setSearch] = useState("");

  // simulação de base de produtos
  const productsMock = [
    { id: 1, name: "Arroz", description: "Arroz branco tipo 1", qty: 1, priority: false },
    { id: 2, name: "Feijão", description: "Feijão carioca", qty: 1, priority: false },
    { id: 3, name: "Macarrão", description: "Macarrão espaguete", qty: 1, priority: false },
    { id: 4, name: "Açúcar", description: "Açúcar refinado", qty: 1, priority: false },
  ];

  const filteredProducts = useMemo(() => {
    if (!search) return [];

    return productsMock.filter((p) =>
      p.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [search]);

  return (
    <Box
      sx={{
        flex: 1,
        bgcolor: "grey.50",
        borderRadius: 3,
        p: 3,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Typography
        textAlign="center"
        fontSize={20}
        fontWeight={500}
      >
        Nova Requisição
      </Typography>

      <Divider sx={{ my: 2 }} />

      {/* BUSCA */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <SearchBar
          value={search}
          onChange={(_, value) => setSearch(value)}
          name="product"
          placeholder="Buscar produto..."
          debounce={300}
        />
      </Box>

      {/* RESULTADOS OU SUGESTÕES */}
      {filteredProducts.length > 0 ? (
        <SearchProductList
          products={filteredProducts}
          onRequestProduct={onSelectSuggestion}
        />
      ) : (
        <PurchaseSuggestions
          suggestions={suggestions}
          onSelectSuggestion={onSelectSuggestion}
        />
      )}
    </Box>
  );
};

export default RequestMainPanel;