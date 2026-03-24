import { Box, Paper } from "@mui/material";
import LoginForm from "../components/LoginForm";
import LogoSvg from "../../../assets/icon/logo_text.svg?react";

const LoginPage = () => {
  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        background: "linear-gradient(244.56deg, #634494 33.22%, #351763 93.06%)",
        pt:2,
        pr:2,
        pb:2
      }}
    >
      <Box
        sx={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Box
          sx={{
            width: 400,
            height: 180,
            borderRadius: 2,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#666",
            fontStyle: "italic",
            fontSize: 24,
          }}
        >
          <LogoSvg/>
        </Box>
      </Box>

      <Box
        sx={{
          flex: 1,
          display: "flex",
          alignItems: "end",
          justifyContent: "flex-end",
        }}
      >
        <Box
          sx={{
            width: "90%",
            height: "100%",
            borderRadius: 3,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "#fff",
          }}
        >
          <LoginForm />
        </Box>
      </Box>
    </Box>
  );
};

export default LoginPage;
