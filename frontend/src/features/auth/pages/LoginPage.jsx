import { Box, Paper } from "@mui/material";
import LoginForm from "../components/LoginForm";

const LoginPage = () => {
  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        backgroundColor: "#d9d9d9",
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
            width: 300,
            height: 180,
            border: "1px solid #999",
            borderRadius: 2,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#666",
            fontStyle: "italic",
            fontSize: 24,
          }}
        >
          LOGO
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
