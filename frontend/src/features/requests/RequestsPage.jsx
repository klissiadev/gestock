import { Box } from "@mui/material";
import { useState, useEffect } from "react";

import { useHeader } from "../../HeaderContext";
import RequestMainPanel from "./components/RequestMainPanel";
import RequestCartPanel from "./components/RequestCartPanel";
import RequestSuccessCard from "./components/RequestSuccessCard";

const RequestPage = () => {

  const [products, setProducts] = useState([]);
  const [requestSent, setRequestSent] = useState(false);
  const { setHeaderConfig } = useHeader();

  useEffect(() => {
    setHeaderConfig({
      variant: "requests",
    });
  }, []);

  const suggestionsMock = [
    { id: 10, name: "Conector USB-C", type: "Matéria prima", qty: 10, priority: true },
    { id: 9, name: "Conector USB", type: "Matéria prima", qty: 20, priority: true },
    { id: 8, name: "Memória Flash", type: "Matéria prima", qty: 25, priority: true },
    { id: 5, name: "LED RGB", type: "Matéria prima", qty: 10, priority: true },
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
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          minHeight: "60vh"
        }}
      >
        <RequestSuccessCard setRequestSent={setRequestSent} />
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
        setRequestSent={setRequestSent}
        onSubmit={() => setRequestSent(true)}
      />
    </Box>
  );}

export default RequestPage;