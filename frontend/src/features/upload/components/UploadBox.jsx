import React from "react";
import { Paper, Stack, Typography, Divider } from "@mui/material";

const UploadBox = () => {
  return (
    <Paper elevation={1}>
      <Stack direction="column" spacing={2}>
        {/* Titulo */}
        <Typography
          variant="h6"
          sx={{
            fontFamily: (theme) => theme.typography.fontFamily,
            fontWeight: (theme) => theme.typography.fontWeightLight,
          }}
        >
          Anexar Arquivos
        </Typography>
        {/* Divisor */}
        <Divider variant="middle" />


      </Stack>
    </Paper>
  );
};

export default UploadBox;
