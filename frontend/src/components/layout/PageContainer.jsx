// frontend\src\components\layout\PageContainer.jsx
import { Box } from "@mui/material";

export default function PageContainer({ children }) {
  return (
    <Box 
        sx={{
            minHeight: 0, 
            bgcolor: 'background.paper',
            borderRadius: 3,
            p: 1 ,
            ml: 2.5,
            mt: 2.5,
            overflow:"auto",
            display: "flex",
            flex: 1,
            width: "calc(100% - 20px)",
        }}
    >
      {children}
    </Box>
  );
}
