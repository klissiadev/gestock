import { Box, Typography, Divider } from "@mui/material";
import SearchBar from "../../stock/components/SearchBar";

const RequestMainPanel = () => {
  return (
    <Box
      sx={{
        flex: 1,
        bgcolor: "grey.50",
        borderRadius: 3,
        p: 3,
        display: "flex",
        flexDirection: "column"
      }}
    >

      <Typography
        textAlign="center"
        fontSize={20} fontWeight={500}
      >
        Nova Requisição
      </Typography>

      <Divider sx={{ my: 2 }} />

      {/* Aqui depois entra a busca e recomendações */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
        }}
      >
        <Box
            sx={{
               flex: 1,
               display: "flex",
               justifyContent: "center",
               height: 42
            }}
        >
            <SearchBar
                value={""}
                onChange={""}
                name="product"
                placeholder="Buscar produto..."
                debounce={300}
            />
        </Box>
      </Box>

    </Box>
  );
};

export default RequestMainPanel;