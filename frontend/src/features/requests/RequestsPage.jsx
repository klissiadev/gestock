import { Box } from "@mui/material";
import { useState, useEffect } from "react";

import { useHeader } from "../../HeaderContext";
import RequestMainPanel from "./components/RequestMainPanel";
import RequestCartPanel from "./components/RequestCartPanel";
import RequestSuccessCard from "./components/RequestSuccessCard";
import { fetchSuggestions } from "../../features/requests/services/suggestionApi";

const RequestPage = () => {

  const [products, setProducts] = useState([]);
  const [requestSent, setRequestSent] = useState(false);
  const { setHeaderConfig } = useHeader();
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setHeaderConfig({
      variant: "requests",
    });
  }, []);

  useEffect(() => {
  let isMounted = true;

  const loadSuggestions = async () => {
      try {
        const data = await fetchSuggestions();
        if (isMounted) {
          setSuggestions(data);
        }
      } catch (error) {
        console.error(error);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadSuggestions();

    return () => {
      isMounted = false;
    };
  }, []); 

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
        suggestions={suggestions}
        onSelectSuggestion={handleSelectSuggestion}
        loadingSuggestions={loading}
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