import {
  Box,
  Typography,
  TextField,
  Button,
  IconButton,
  InputAdornment,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import StepContainer from "./StepContainer";
import { useState, useMemo } from "react";
import { cancel_button, accept_button } from "../styles/style";

export default function StepCriarSenha({ onNext, onBack }) {
  const [senha, setSenha] = useState("");
  const [confirmSenha, setConfirmSenha] = useState("");
  const [showSenha, setShowSenha] = useState(false);
  const [showConfirmSenha, setShowConfirmSenha] = useState(false);

  const validations = useMemo(() => {
    return {
      length: senha.length >= 8 && senha.length <= 12,
      uppercase: /[A-Z]/.test(senha),
      number: /[0-9]/.test(senha),
      match: senha === confirmSenha && senha !== "",
    };
  }, [senha, confirmSenha]);

  const senhaValida =
    validations.length &&
    validations.uppercase &&
    validations.number &&
    validations.match;

  const handleNext = () => {
    if (!senhaValida) return;
    onNext();
  };

  return (
    <StepContainer>
      <Box
        display="flex"
        alignItems="center"
        justifyContent="space-between"
        mb={2}
      >
        <IconButton
          size="small"
          onClick={onBack}
          sx={{
            color: "#000",
            backgroundColor: (theme) => theme.palette.button.main,
          }}
        >
          <ArrowBackIcon fontSize="small" />
        </IconButton>

        <Typography fontSize={20} color="#000" textAlign="center">
          Criar Senha
        </Typography>
        <Box />
      </Box>

      <Box display="flex" flexDirection="column" gap={1} px={4}>
        <Typography fontSize={15} fontWeight={300}>
          Senha
        </Typography>

        <TextField
          type={showSenha ? "text" : "password"}
          size="small"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          sx={{ mb: 2, height: "26px"}}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  size="small"
                  onClick={() => setShowSenha(!showSenha)}
                >
                  {showSenha ? (
                    <VisibilityOffIcon fontSize="small" />
                  ) : (
                    <VisibilityIcon fontSize="small" />
                  )}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <Typography fontSize={15} fontWeight={300}>
          Confirmar Senha
        </Typography>

        <TextField
          type={showConfirmSenha ? "text" : "password"}
          size="small"
          value={confirmSenha}
          onChange={(e) => setConfirmSenha(e.target.value)}
          error={!validations.match && confirmSenha !== ""}
          helperText={
            !validations.match && confirmSenha !== ""
              ? "As senhas não coincidem"
              : ""
          }
          sx={{ mb: 2, height: "26px" }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  size="small"
                  onClick={() =>
                    setShowConfirmSenha(!showConfirmSenha)
                  }
                >
                  {showConfirmSenha ? (
                    <VisibilityOffIcon fontSize="small" />
                  ) : (
                    <VisibilityIcon fontSize="small" />
                  )}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <Box mt={1}>
          <Typography variant="body2" mb={1}>
            Sua senha deve conter:
          </Typography>

          <Typography
            variant="caption"
            display="block"
            sx={{
              textDecoration: validations.length
                ? "none"
                : "line-through",
              color: validations.length ? "green" : "error.main",
            }}
          >
            8 a 12 caracteres
          </Typography>

          <Typography
            variant="caption"
            display="block"
            sx={{
              textDecoration: validations.uppercase
                ? "none"
                : "line-through",
              color: validations.uppercase ? "green" : "error.main",
            }}
          >
            1 letra maiúscula
          </Typography>

          <Typography
            variant="caption"
            display="block"
            sx={{
              textDecoration: validations.number
                ? "none"
                : "line-through",
              color: validations.number ? "green" : "error.main",
            }}
          >
            1 número
          </Typography>
        </Box>
      </Box>

      <Box
        display="flex"
        flexDirection="row"
        gap={2}
        mt={4}
        mr={4}
        width={"70%"}
        justifySelf={"flex-end"}
      >
        <Button sx={cancel_button}>Cancelar</Button>
        <Button
          sx={accept_button}
          onClick={handleNext}
        >
          Próximo
        </Button>
      </Box>
    </StepContainer>
  );
}