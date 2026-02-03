
import { Stack, Divider, Typography } from "@mui/material";
import { stack_principal } from "./styles/style";
import UploadDialog from "./pages/UploadDialog";
import { useFileUpload } from "./hooks/useFileManager";

const UploadPageDebug = () => {
  return (
    <Stack
      direction="column"
      spacing={2}
      alignItems="center"
      sx={stack_principal}
    >

      <Typography
        variant="h6"
        sx={{
          fontFamily: (theme) => theme.typography.fontFamily,
          fontWeight: (theme) => theme.typography.fontWeightLight,
        }}
      >
        Upload de Planilhas
      </Typography>

      <Divider variant="middle" />

      {/* Quadrado de upload */}
      <UploadDialog/>

    </Stack>
  );
};

export default UploadPageDebug;
