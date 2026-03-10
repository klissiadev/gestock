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
import { toast } from "react-toastify";
import FuncaoSelector from "./FuncaoSelector";

export default function StepDadosGerais({ data, updateData, onNext }) {
  const [submitted, setSubmitted] = useState(false);

  const isValidEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };

  const handleNext = () => {
    setSubmitted(true);

    console.log("Dados: ", data)

    const nomeValido = data.nome.trim() !== "";
    const emailPreenchido = data.email.trim() !== "";
    const emailValido = isValidEmail(data.email.trim());

    if (!nomeValido) {
      toast.error("O nome é obrigatório.");
      return;
    }

    if (!emailPreenchido) {
      toast.error("O email é obrigatório.");
      return;
    }

    if (!emailValido) {
      toast.error("Digite um email válido.");
      return;
    }

    if (!data.papel) {
      toast.error("Selecione uma função.");
      return;
    }



    onNext();
  };

  return (
    <StepContainer>
      <Typography fontSize={20} color="#000" textAlign="center" mb={1}>
        Dados Pessoais
      </Typography>

      <Box display="flex" flexDirection="column" gap={1} px={4}>

        <Typography fontSize={15} fontWeight={300} >Nome Completo</Typography>
        <TextField
          size="small"
          value={data.nome}
          onChange={(e) => updateData({ nome: e.target.value })}
          error={submitted && data.nome.trim() === ""}
          helperText={
            submitted && data.nome.trim() === ""
              ? "Nome é obrigatório"
              : ""
          }
        />
        <Typography fontSize={15} fontWeight={300}>Email</Typography>
        <TextField
          size="small"
          value={data.email}
          onChange={(e) => updateData({ email: e.target.value })}
          error={
            submitted &&
            (
              data.email.trim() === "" ||
              !isValidEmail(data.email.trim())
            )
          }
          helperText={
            submitted && data.email.trim() === ""
              ? "Email é obrigatório"
              : submitted && !isValidEmail(data.email.trim())
              ? "Email inválido"
              : ""
          }
        />
        <FuncaoSelector
          value={data.papel}
          onChange={(value) => updateData({ papel: value })}
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
