import {
  Box,
  Typography,
  TextField,
  Button,
  IconButton,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import StepContainer from "./StepContainer";

const PASSWORD_RULES = [
  "de 8 a 12 caracteres",
  "1 letra maiúscula",
  "1 número",
];

export default function StepCriarSenha({ onNext, onBack }) {
  return (
    <StepContainer>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <IconButton size="small" onClick={onBack}>
          <ArrowBackIcon fontSize="small" />
        </IconButton>

        <Typography variant="h6">Criar Senha</Typography>
      </Box>

      <Box display="flex" flexDirection="column" gap={2}>
        <TextField
          label="Senha"
          type="password"
          size="small"
          InputProps={{
            endAdornment: (
              <IconButton size="small">
                <VisibilityIcon fontSize="small" />
              </IconButton>
            ),
          }}
        />

        <TextField
          label="Confirmar senha"
          size="small"
          type="password"
          InputProps={{
            endAdornment: (
              <IconButton size="small">
                <VisibilityOffIcon fontSize="small" />
              </IconButton>
            ),
          }}
        />

        <Box mt={2}>
          <Typography variant="body2" mb={1}>
            Sua senha deve conter
          </Typography>

          {PASSWORD_RULES.map((rule) => (
            <Typography key={rule} variant="caption" display="block">
              ✓ {rule}
            </Typography>
          ))}
        </Box>

        <Box display="flex" justifyContent="space-between" mt={3}>
          <Button variant="outlined">Cancelar</Button>
          <Button variant="contained" onClick={onNext}>
            Próximo
          </Button>
        </Box>
      </Box>
    </StepContainer>
  );
}
