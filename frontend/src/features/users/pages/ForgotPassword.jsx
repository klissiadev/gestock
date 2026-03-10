import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Paper, Typography, TextField, Button, Stack, CircularProgress } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useAuth } from "../../../AuthContext"
import { accept_button, cancel_button } from "../styles/style"; // Reaproveitando seus estilos

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [isSent, setIsSent] = useState(false); // Para mostrar mensagem de sucesso
  const { sendRecoveryEmail, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) return;

    const success = await sendRecoveryEmail(email);
    if (success) {
      setIsSent(true);
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      sx={{ height: "100vh", backgroundColor: "#FFFFFF", px: 2 }}
    >
      <Paper elevation={2}  sx={{ width: "100%", maxWidth: 400, p: 4 }}>
        {/* Botão Voltar */}
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate("/login")}
          sx={{ color: "#000", mb: 4, textTransform: "none" }}
        >
          Voltar para o Login
        </Button>

        {!isSent ? (
          <Stack spacing={3}>
            <Box>
              <Typography variant="h4" fontWeight="bold" gutterBottom>
                Esqueceu a senha?
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Digite seu e-mail abaixo. Se ele estiver cadastrado no Gestock, 
                enviaremos um link para você criar uma nova senha.
              </Typography>
            </Box>

            <form onSubmit={handleSubmit}>
              <Stack spacing={3}>
                <TextField
                  fullWidth
                  label="Seu E-mail"
                  type="email"
                  variant="outlined"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  error={!!error}
                  helperText={error}
                />

                <Button
                  fullWidth
                  type="submit"
                  variant="contained"
                  disabled={loading}
                  sx={accept_button}
                >
                  {loading ? <CircularProgress size={24} color="inherit" /> : "Enviar link de recuperação"}
                </Button>
              </Stack>
            </form>
          </Stack>
        ) : (
          // 💡 Mensagem de Sucesso (Feedback após enviar)
          <Stack spacing={3} textAlign="center">
            <Typography variant="h5" fontWeight="bold" color="green">
              E-mail enviado!
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Verifique sua caixa de entrada (e a pasta de spam) em <strong>{email}</strong>. 
              Siga as instruções no e-mail para redefinir sua senha.
            </Typography>
            <Button
              variant="outlined"
              onClick={() => navigate("/login")}
              sx={cancel_button}
            >
              Entendido
            </Button>
          </Stack>
        )}
      </Paper>
    </Box>
  );
};

export default ForgotPassword;