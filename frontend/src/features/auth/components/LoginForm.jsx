import { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  InputAdornment
} from "@mui/material";
import ErrorOutlineIcon from "../../../assets/icon/iconError.svg?react";
import { sendCredencials } from "../service/loginService";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email || !password) {
      setError(true);
      return;
    }

    setError(false);
    console.log("Login:", { email, password });

    sendCredencials(email, password);


  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        width: "100%",
        display: "flex",
        flexDirection: "column",
        gap: 1,
        padding: 10
      }}
    >
      <Box
        sx={{
          width: 50,
          height: 50,
          border: "1px solid #bbb",
          borderRadius: 2,
          alignSelf: "center",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 10,
          color: "#888",
        }}
      >
        ÍCONE
      </Box>

      <Typography variant="body2">Email</Typography>
      <TextField
        placeholder="Insira seu email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={error}
        InputProps={{
            endAdornment: error && (
            <InputAdornment position="end">
                <ErrorOutlineIcon width={18} height={18} />
            </InputAdornment>
            ),
        }}
        />


        <Typography variant="body2">Senha</Typography>
        <TextField
            placeholder="Insira sua senha"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            error={error}
            InputProps={{
                endAdornment: error && (
                <InputAdornment position="end">
                    <ErrorOutlineIcon width={18} height={18} />
                </InputAdornment>
                ),
            }}
        />

      {error && (
        <Typography fontSize={11} color="red">
          Usuário ou Senha incorretos. Tente novamente ou entre em contato com o ADM.
        </Typography>
      )}

      <Button
        type="submit"
        variant="contained"
        sx={{
          mt: 4,
          width: "100%",
          color: "#fff",
          fontWeight: 500,
          textTransform: "none",
          backgroundColor: "#6b6b6b",
          borderRadius:"8px",
          "&:hover": {
            backgroundColor: "#555",
          },
        }}
      >
        Entrar
      </Button>
    </Box>
  );
};

export default LoginForm;
