import { Box, Typography, Divider, CircularProgress } from "@mui/material";
import { useState } from "react";

import SearchBar from "../../stock/components/SearchBar";
import PurchaseSuggestions from "./PurchaseSuggestions";
import SearchProductList from "./SearchProductList";
import { useProductSearch } from "../hooks/useProductSearch";

const RequestMainPanel = ({ suggestions, onSelectSuggestion }) => {

  const [search, setSearch] = useState("");

  const { products, loading } = useProductSearch(search);

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
      <Typography textAlign="center" fontSize={20} fontWeight={500}>
        Nova Requisição
      </Typography>

      <Divider sx={{ my: 2 }} />

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

      {/* LOADING */}
      {loading && (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress size={28} />
        </Box>
      )}

      {/* RESULTADOS */}
      {!loading && search && products.length > 0 && (
        <SearchProductList
          products={products}
          onRequestProduct={onSelectSuggestion}
        />
      )}

      {/* NENHUM RESULTADO */}
      {!loading && search && products.length === 0 && (
        <Box mt={4} textAlign="center">
          <Typography color="text.secondary" fontSize={14}>
            Produto não encontrado
          </Typography>
        </Box>
      )}

      {/* SUGESTÕES */}
      {!search && (
        <PurchaseSuggestions
          suggestions={suggestions}
          onSelectSuggestion={onSelectSuggestion}
        />
      )}
    </Box>
  );
};

export default RequestMainPanel;