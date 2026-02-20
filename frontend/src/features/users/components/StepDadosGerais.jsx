import {
  Box,
  Typography,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import StepContainer from "./StepContainer";
import { cancel_button, accept_button} from "../styles/style";
import { useState } from "react";


export default function StepDadosGerais({ onNext }) {

    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [matricula, setMatricula] = useState("");
    const [submitted, setSubmitted] = useState(false);

    const isNomeInvalid = submitted && !nome.trim();
    const isEmailInvalid = submitted && !email.trim();
    const isMatriculaInvalid = submitted && !matricula.trim();

    const handleNext = () => {
        setSubmitted(true);

        if (nome.trim() && email.trim() && matricula.trim()) {
        onNext();
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
            sx={{height: "26px", mb: 2}} 
            size="small" 
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            error={isNomeInvalid}
            placeholder={isNomeInvalid ? "Campo Obrigatório *" : ""}
        />
        <Typography fontSize={15} fontWeight={300}>Email</Typography>
        <TextField 
            sx={{height: "26px", mb: 2}} 
            size="small" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            error={isEmailInvalid}
            placeholder={isEmailInvalid ? "Campo Obrigatório *" : ""}
        />
        <Typography fontSize={15} fontWeight={300}>Número de Matrícula</Typography>
        <TextField
            sx={{height: "26px", mb: 2}} 
            size="small" 
            value={matricula}
            onChange={(e) => setMatricula(e.target.value)}
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
