import {
  Box,
  Typography,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import StepContainer from "./StepContainer";
import { cancel_button, accept_button } from "../styles/style";
import { useState } from "react";


export default function StepDadosGerais({ data, updateData, onNext }) {
  const [submitted, setSubmitted] = useState(false);
  const isMatriculaInvalid = submitted && !data.matricula.trim();

  const handleNext = () => {
    setSubmitted(true);
    if (data.nome.trim() && data.email.trim() && data.matricula.trim()) {
      onNext();
    }
    else {
      console.log("ta invado: ", (data.nome.trim() && data.email.trim() && data.matricula.trim()))
      console.log("nome: ", data.nome.trim());
      console.log("email: ", data.email.trim());
      console.log("matricula: ",  data.matricula.trim());
    }
  };

  return (
    <StepContainer>
      <Typography fontSize={20} color="#000" textAlign="center" mb={1}>
        Dados Pessoais
      </Typography>

      <Box display="flex" flexDirection="column" gap={1} px={4}>

        <Typography fontSize={15} fontWeight={300} >Nome Completo</Typography>
        <TextField
          sx={{ height: "26px", mb: 2 }}
          size="small"
          value={data.nome}
          onChange={(e) => updateData({ nome: e.target.value })}
          error={submitted && !data.nome.trim()}
          placeholder={(submitted && !data.nome.trim()) ? "Campo Obrigatório *" : ""}
        />
        <Typography fontSize={15} fontWeight={300}>Email</Typography>
        <TextField
          sx={{ height: "26px", mb: 2 }}
          size="small"
          value={data.email}
          onChange={(e) => updateData({ email: e.target.value })}
          error={submitted && !data.email.trim()}
          placeholder={(submitted && !data.email.trim()) ? "Campo Obrigatório *" : ""}
        />
        <Typography fontSize={15} fontWeight={300}>Número de Matrícula</Typography>
        <TextField
          sx={{ height: "26px", mb: 2 }}
          size="small"
          value={data.matricula}
          onChange={(e) => updateData({ matricula: e.target.value })}
          error={isMatriculaInvalid}
          placeholder={isMatriculaInvalid ? "Campo Obrigatório *" : ""}
        />

      </Box>

      <Box display="flex" flexDirection="row" gap={2} justifySelf={"flex-end"} mt={10} mr={4} width={"70%"} >
        <Button sx={cancel_button}>Cancelar</Button>
        <Button sx={accept_button} onClick={handleNext}>
          Próximo
        </Button>
      </Box>
    </StepContainer>
  );
}
