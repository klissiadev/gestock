import { Box } from "@mui/material";

export default function StepContainer({ children }) {
  return (
    <Box
      sx={{
        width: 520,
        height:"100%",
        backgroundColor: (theme) => theme.palette.uploadBox.main,
        borderRadius: 2,
        p: 4,
        mx: "auto",
        alignItems:"center",
        justifyContent:"center"
      }}
    >
      {children}
    </Box>
  );
}
