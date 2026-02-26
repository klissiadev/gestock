import React from 'react'
import { useState } from "react";

import { Box, Stack } from "@mui/material";
import RegisterUserBar from "../components/RegisterUserBar";
import StepProgress from "../components/StepProgress";
import StepDadosGerais from "../components/StepDadosGerais";
import StepCriarSenha from "../components/StepCriarSenha";
import StepConcluido from "../components/StepConcluido";


const RegisterUserPage = () => {
  const [activeStep, setActiveStep] = useState(1);

  const handleNext = () => setActiveStep((prev) => prev + 1);
  const handleBack = () => setActiveStep((prev) => prev - 1);

  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    papel: "",
    password: "",
  });

  const updateFormData = (newData) => {
    setFormData((prev) => ({ ...prev, ...newData }));
  };

  return (
    <Stack
      direction="column"
      spacing={2}
      sx={{
        backgroundColor: (theme) => theme.palette.common.white,
        padding: 2,
        flex: 1,
        height: "100vh",
        width: "100%",
      }}
    >
      <RegisterUserBar
        titulo={"Adicionar Usuário"}
      />

      <StepProgress activeStep={activeStep} />
      <Box
        sx={{
          alignContent: 'center',
          height: "100%"
        }}
      >
        {activeStep === 1 && 
        <StepDadosGerais
          data={formData}
          updateData={updateFormData}
          onNext={handleNext} 
          />}

        {activeStep === 2 && (
          <StepCriarSenha 
          data={formData} 
          updateData={updateFormData}
          onNext={handleNext} 
          onBack={handleBack} 
          mode="register"/>
          
        )}
        {activeStep === 3 && <StepConcluido />}
      </Box>
    </Stack>
  )
}

export default RegisterUserPage