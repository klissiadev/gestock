import React from 'react'
import { useState } from "react";

import { Box, Stack } from "@mui/material";
import RegisterUserBar from "../components/RegisterUserBar";
import StepProgress from "../components/StepProgress";
import StepDadosGerais from "../components/StepDadosGerais";
import StepCriarSenha from "../components/StepCriarSenha";
import StepConcluido from "../components/StepConcluido";


const RegisterUserPage = () => {
  const [activeStep, setActiveStep] = useState(() => {
    const saved = localStorage.getItem("register_step");
    return saved ? parseInt(saved) : 1;
  });

  const handleNext = () => {
    setActiveStep((prev) => {
      const next = prev + 1;
      localStorage.setItem("register_step", next);
      return next;
    });
  };

  const handleBack = () => {
  setActiveStep((prev) => {
    const next = prev - 1;
    localStorage.setItem("register_step", next);
    return next;
  });
};

  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    papel: "",
    password: "",
  });

  const updateFormData = (newData) => {
    setFormData((prev) => ({ ...prev, ...newData }));
    console.log("Active Step agora: ", activeStep);
  };

  return (
    <Stack
      direction="column"
      spacing={2}
      sx={{
        backgroundColor: (theme) => theme.palette.common.white,
        padding: 2,
        flex: 1,
        height: "80vh",
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
            mode="register" />

        )}
        {activeStep === 3 && <StepConcluido />}
      </Box>
    </Stack>
  )
}

export default RegisterUserPage