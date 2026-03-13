import { Box, TextField, Typography, Button } from "@mui/material";
import { useState } from "react";
import { createRequest } from "../services/requestApi";

const RequestForm = ({ products, setRequestSent }) => {

  const [titulo, setTitulo] = useState("");
  const [observacao, setObservacao] = useState("");

  const handleSubmit = async () => {
    try {
      if (products.length === 0) {
        alert("Adicione produtos antes de enviar");
        return;
      }
      const payload = {
        titulo,
        observacao,
        itens: products.map((p) => ({
          produto_id: p.id,
          quantidade: p.qty,
          prioridade: p.priority,
        })),
      };

      const result = await createRequest(payload);
      setRequestSent(true); 

      console.log("Requisição criada:", result);

    } catch (error) {
      console.error("Erro ao enviar requisição:", error);
    }
  };

  return (
    <Box
      sx={{
        p: 2,
        borderTop: "1px solid",
        borderColor: "divider",
        display: "flex",
        flexDirection: "column",
        gap: 2,
        alignItems: "center",
      }}
    >

      <TextField
        size="small"
        placeholder="Título"
        fullWidth
        value={titulo}
        onChange={(e) => setTitulo(e.target.value)}
      />

      <TextField
        placeholder="Observações"
        multiline
        minRows={1}
        maxRows={6}
        fullWidth
        value={observacao}
        onChange={(e) => setObservacao(e.target.value)}
      />

      <Typography fontSize={12} color="text.secondary" textAlign={"center"}>
        {products.length} produtos foram adicionados
      </Typography>

      <Button
        variant="contained"
        fullWidth
        onClick={handleSubmit}
        sx={{
          borderRadius: "12px",
          textTransform: "none",
          flex: 1,
          height: 40,
          fontFamily: (theme) => theme.typography.fontFamily,
          fontWeight: (theme) => theme.typography.fontWeightLight,
          color: (theme) => theme.palette.common.white,
          backgroundColor: (theme) => theme.palette.uploadBox.button,
          "&:hover": {
            backgroundColor: (theme) => theme.palette.button.hover,
            color: (theme) => theme.palette.common.black,
          },
        }}
      >
        Enviar
      </Button>

    </Box>
  );
};

export default RequestForm;