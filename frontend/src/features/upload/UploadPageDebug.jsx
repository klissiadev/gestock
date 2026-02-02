import React from "react";
import {
  Stack,
  Typography,
  Divider,
  Paper,
  Box,
  Select,
  MenuItem,
  Button,
} from "@mui/material";
import { stack_principal } from "./styles/style";
import { theme } from "../../style/theme";

const UploadPageDebug = () => {
  return (
    <Stack
      direction="column"
      spacing={2}
      alignItems="center"
      sx={{
        backgroundColor: (theme) => theme.palette.common.white,
        width: "100%",
        padding: 1,
        textAlign: "center",
      }}
    >
      {/* Titulo */}
      <Typography
        variant="h6"
        sx={{
          fontFamily: (theme) => theme.typography.fontFamily,
          fontWeight: (theme) => theme.typography.fontWeightLight,
        }}
      >
        Upload de Planilhas
      </Typography>
      {/* Divisor */}
      <Divider variant="middle" />

      {/* Quadrado de upload */}
      <Paper
        elevation={1}
        sx={{
          maxWidth: 500,
          mx: "auto",
          p: 12,
          borderRadius: 3,
          boxShadow: 3,
        }}
      >
        <Stack direction="column" spacing={2}>
          <Typography
            variant="h6"
            sx={{
              fontFamily: (theme) => theme.typography.fontFamily,
              fontWeight: (theme) => theme.typography.fontWeightMedium,
              textAlign: "center",
            }}
          >
            Anexar Arquivos
          </Typography>

          <Divider />

          {/* Aqui entra a dropzone */}
          <Stack direction="column" spacing={2} alignItems="center">
            {/* Texto anexar */}
            <Typography
              sx={{
                fontFamily: (theme) => theme.typography.fontFamily,
                fontWeight: (theme) => theme.typography.fontWeightLight,
                textAlign: "center",
              }}
            >
              Envie seus arquivos .csv ou .xlsx
            </Typography>

            {/* Select Tipo do arquivo */}
            <Select value={"a"} placeholder="Produtos">
              <MenuItem value={"a"}>LOREM IPSUM BLA BLA BNLA</MenuItem>
              <MenuItem value={"b"}>B</MenuItem>
              <MenuItem value={"c"}>C</MenuItem>
            </Select>

            {/* Box pontilhada escrita "Arraste aqui os arquivos" */}
            <Box
              sx={{
                borderStyle: "dashed",
                borderWidth: "2px",
                borderRadius: 4,
                borderColor: (theme) => theme.palette.button.main,
                padding: 10,
              }}
            >
              <Typography
                sx={{
                  fontFamily: (theme) => theme.typography.fontFamily,
                  fontWeight: (theme) => theme.typography.fontWeightLight,
                  textAlign: "center",
                }}
              >
                Arraste seus arquivos aqui
              </Typography>
            </Box>

            {/* Botao 'procure nesse dispositivo" */}
            <Button
              sx={{
                width: 240,
                backgroundColor: (theme) => theme.palette.button.main,
                "&:hover": {
                  backgroundColor: (theme) => theme.palette.button.hover,
                },
                fontFamily: (theme) => theme.typography.fontFamily,
                fontWeight: (theme) => theme.typography.fontWeightLight,
                fontSize: 13,
                padding: 2,
              }}
            >
              Procurar nesse dispositivo
            </Button>

            {/* Botoes cancelar e Enviar */}
            <Stack spacing={2} direction={"row"}>
              <Button
                sx={{
                  backgroundColor: (theme) => theme.palette.button.main,
                  "&:hover": {
                    backgroundColor: (theme) => theme.palette.button.hover,
                  },
                  fontFamily: (theme) => theme.typography.fontFamily,
                  fontWeight: (theme) => theme.typography.fontWeightLight,
                  fontSize: 13,
                  padding: 2,
                }}
              >
                Cancelar
              </Button>
              <Button
                sx={{
                  backgroundColor: (theme) => theme.palette.background.default,
                  "&:hover": {
                    backgroundColor: (theme) => theme.palette.button.hover,
                  },
                  fontFamily: (theme) => theme.typography.fontFamily,
                  fontWeight: (theme) => theme.typography.fontWeightLight,
                  fontSize: 13,
                  padding: 2,
                }}
              >
                Enviar
              </Button>
            </Stack>
          </Stack>
        </Stack>
      </Paper>
    </Stack>
  );
};

export default UploadPageDebug;
