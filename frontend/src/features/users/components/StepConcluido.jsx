import { Box, Typography, Button } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import StepContainer from "./StepContainer";
import { accept_button} from "../styles/style";

export default function StepConcluido() {
  return (
    <StepContainer>
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" gap={2} height={"100%"}>

        <Box display="flex" flexDirection="row" alignItems="center" justifyContent="center" gap={2}>
           <CheckCircleIcon sx={{ fontSize: 40, background: (theme) => theme.palette.uploadBox.main }} />
            <Typography variant="h6" fontWeight={500}>Usuário Salvo</Typography> 
        </Box>
        

        <Typography variant="body2" textAlign="center">
          Cadastro realizado com sucesso!
          <br />
          A conta foi criada e já pode ser acessada pelo usuário.
        </Typography>

        <Box mt={4}  width={"100%"} align={'center'} >
            <Button sx={accept_button}>
                Voltar para usuários
            </Button>
        </Box>
      </Box>
    </StepContainer>
  );
}
