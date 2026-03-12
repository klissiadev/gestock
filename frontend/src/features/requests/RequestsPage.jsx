import { Box } from "@mui/material";
import { useState } from "react";

import RequestMainPanel from "./components/RequestMainPanel";
import RequestCartPanel from "./components/RequestCartPanel";
import RequestSuccessCard from "./components/RequestSuccessCard";

const RequestPage = () => {

  const [products, setProducts] = useState([]);
  const [requestSent, setRequestSent] = useState(false);

  const suggestionsMock = [
    { id: 1, name: "Arroz", type: "Arroz branco tipo 1", qty: 1, priority: false },
    { id: 2, name: "Feijão", type: "Feijão carioca", qty: 1, priority: false },
    { id: 3, name: "Macarrão", type: "Macarrão espaguete", qty: 1, priority: false },
    { id: 4, name: "Açúcar", type: "Açúcar refinado", qty: 1, priority: false },
  ];

  const handleSelectSuggestion = (product) => {
    setProducts((prev) => {
      if (prev.some((p) => p.id === product.id)) return prev;
      return [...prev, product];
    });
  };

  if (requestSent) {
    return (
      <Box
        height="85vh"
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <RequestSuccessCard />
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: "flex",
        gap: 2,
        height: "85vh",
        width: "100%",
      }}
    >
      <RequestMainPanel
        suggestions={suggestionsMock}
        onSelectSuggestion={handleSelectSuggestion}
      />

      <RequestCartPanel
        products={products}
        setProducts={setProducts}
        onSubmit={() => setRequestSent(true)}
      />
    </Box>
  );
};

export default RequestPage;