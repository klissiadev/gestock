import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Box, Typography } from "@mui/material";
import StepCriarSenha from "../components/StepCriarSenha"
import { useAuth } from "../../../AuthContext"; 

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { resetPassword } = useAuth(); 

  const token = searchParams.get("token"); // Pega o token da URL automaticamente

  const [recoveryData, setRecoveryData] = useState({
    password: "",
  });

  const handleReset = async () => {
    if (!token) {
      alert("Token inválido ou expirado.");
      return;
    }

    const success = await resetPassword(token, recoveryData.password);
    
    if (success) {
      alert("Senha alterada com sucesso!");
      navigate("/login");
    } else {
      alert("Erro ao redefinir senha. Tente solicitar um novo link.");
    }
  };

  return (
    <Box 
      display="flex" 
      flexDirection="column" 
      alignItems="center" 
      justifyContent="center" 
      sx={{ height: '100%', width: '100%'}}
    >
      <Box sx={{ flex: 1, p: 3, bgcolor: 'white', borderRadius: 2, boxShadow: 3 }}>
        <Typography variant="h5" textAlign="center" mb={3}>
          Redefinir Senha
        </Typography>

        <StepCriarSenha
          data={recoveryData} 
          updateData={(newData) => setRecoveryData(prev => ({ ...prev, ...newData }))}
          onNext={handleReset} // 💡 No modo recovery, o onNext dispara o reset
          mode="recovery"
          customTitle="Nova Senha"
        />
      </Box>
    </Box>
  );
};

export default ResetPassword;