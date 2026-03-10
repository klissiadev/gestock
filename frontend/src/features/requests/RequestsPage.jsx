import { Box } from "@mui/material";

import RequestMainPanel from "./components/RequestMainPanel";
import RequestCartPanel from "./components/RequestCartPanel";

const RequestPage = () => {

  const productsMock = [
    { id: 1, name: "Nome produto", description: "Descrição do produto", qty: 2, priority: false },
    { id: 2, name: "Nome produto", description: "Descrição do produto", qty: 5, priority: true },
    { id: 3, name: "Nome produto", description: "Descrição do produto", qty: 10, priority: true },
    { id: 4, name: "Nome produto", description: "Descrição do produto", qty: 150, priority: false },
    { id: 5, name: "Nome produto", description: "Descrição do produto", qty: 2, priority: true }
  ];

  return (
    <Box
      sx={{
        display: "flex",
        gap: 2,
        height: "85vh",
        width: "100%",
      }}
    >
      <RequestMainPanel />
      <RequestCartPanel productsMock={productsMock} />
    </Box>
  );
};

export default RequestPage;