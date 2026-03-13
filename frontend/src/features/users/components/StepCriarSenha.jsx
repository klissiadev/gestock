import { Box, Typography, TextField, Button, 
  IconButton, InputAdornment, CircularProgress } from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import StepContainer from "./StepContainer";
import { useState, useMemo } from "react";
import { cancel_button, accept_button } from "../styles/style";
import { useAuth } from "../../../AuthContext";
import ValidationLabel from "./ValidationLabel";

export default function StepCriarSenha({
  data, updateData,
  onNext, onBack,
  mode = "register", customTitle // Pra reutilizacao
}) {
  const { register, loading } = useAuth();
  const [confirmSenha, setConfirmSenha] = useState("");
  const [showSenha, setShowSenha] = useState(false);
  const [showConfirmSenha, setShowConfirmSenha] = useState(false);

  // Garante que password não quebre se data vier vazio
  const passwordValue = data?.password || "";

  const validations = useMemo(() => {
    return {
      length: passwordValue.length >= 8 && passwordValue.length <= 12,
      uppercase: /[A-Z]/.test(passwordValue),
      number: /[0-9]/.test(passwordValue),
      match: passwordValue === confirmSenha && passwordValue !== "",
    };
  }, [passwordValue, confirmSenha]);

  const senhaValida =
    validations.length &&
    validations.uppercase &&
    validations.number &&
    validations.match;

  const handleAction = async (e) => {
    if (e && e.preventDefault) e.preventDefault();

    if (!senhaValida) return;

    if (mode === "register") {
      const result = await register(data.nome, data.email, data.password, data.papel);
      if (result.success) {
        console.log("tela de sucesso ");
        onNext();
      }
    }
    else if (mode === "recovery") {
      // const result = await resetPassword(data.token, data.password);
      onNext();
    }
  };

  const displayTitle = customTitle || (mode === "register" ? "Criar Senha" : "Nova Senha");

  return (
    <StepContainer>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        {/* Só mostra o voltar se houver uma função onBack */}
        {onBack ? (
          <IconButton
            size="small"
            onClick={onBack}
            sx={{ color: "#000", backgroundColor: (theme) => theme.palette.button.main }}
          >
            <ArrowBackIcon fontSize="small" />
          </IconButton>
        ) : <Box width={32} />}

        <Typography fontSize={20} color="#000" textAlign="center">
          {displayTitle}
        </Typography>
        <Box width={32} />
      </Box>

      <Box display="flex" flexDirection="column" gap={1} px={4}>
        <Typography fontSize={15} fontWeight={300}>Senha</Typography>
        <TextField
          type={showSenha ? "text" : "password"}
          size="small"
          value={passwordValue}
          onChange={(e) => updateData({ password: e.target.value })}
          sx={{ mb: 2, height: "26px" }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton size="small" onClick={() => setShowSenha(!showSenha)}>
                  {showSenha ? <VisibilityOffIcon fontSize="small" /> : <VisibilityIcon fontSize="small" />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <Typography fontSize={15} fontWeight={300}>Confirmar Senha</Typography>
        <TextField
          type={showConfirmSenha ? "text" : "password"}
          size="small"
          value={confirmSenha}
          onChange={(e) => setConfirmSenha(e.target.value)}
          error={!validations.match && confirmSenha !== ""}
          helperText={!validations.match && confirmSenha !== "" ? "As senhas não coincidem" : ""}
          sx={{ mb: 2, height: "26px" }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton size="small" onClick={() => setShowConfirmSenha(!showConfirmSenha)}>
                  {showConfirmSenha ? <VisibilityOffIcon fontSize="small" /> : <VisibilityIcon fontSize="small" />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        {/* Regras de Validação Visuais */}
        <Box mt={1}>
          <Typography variant="body2" mb={1}>Sua senha deve conter:</Typography>
          <ValidationLabel label="8 a 12 caracteres" isValid={validations.length} />
          <ValidationLabel label="1 letra maiúscula" isValid={validations.uppercase} />
          <ValidationLabel label="1 número" isValid={validations.number} />
        </Box>
      </Box>

      <Box display="flex" flexDirection="row" gap={2} mt={4} mr={4} width={"70%"} justifySelf={"flex-end"}>
        <Button sx={cancel_button} onClick={onBack}>Cancelar</Button>
        <Button
          type="button"
          sx={accept_button}
          onClick={(e) => handleAction(e)}
          disabled={!senhaValida || loading}
        >
          {loading ? <CircularProgress size={24} /> : (mode === "register" ? "Concluir" : "Salvar")}
        </Button>
      </Box>
    </StepContainer>
  );
}

