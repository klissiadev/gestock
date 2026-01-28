import { Box } from "@mui/material";

export default function PageContainer({ children }) {
  return (
    <Box 
        sx={{
            height: "calc(103vh - 153px)",
            bgcolor: 'background.paper',
            borderRadius: 3,
            p: 3,
            ml: 10.5,
            mt: 2.5,
            overflow:"auto",
            display: "flex",
            flex: 1,
        }}
    >
      {children}
    </Box>
  );
}
