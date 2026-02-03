import React from 'react';
import { Paper, Stack, Typography, Divider, Button, } from '@mui/material'
import TypeSelector from "../components/TypeSelector";
import DragBox from "../components/DragBox";
import { button_model, cancel_button, accept_button } from "../styles/style";

const UploadDialog = () => {
  return (
    <Paper
      elevation={1}
      sx={{
        backgroundColor: theme => theme.palette.uploadBox.main,
        maxWidth: 500,
        mx: "auto",
        p: 4,
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
          <TypeSelector
            name="sheet_selector"
            value={"produtos"}
            onChange={null}
            placeholder="Todas as Categorias"
            options={[
              { value: "produtos", label: "Produtos" },
              { value: "movimentacoes_entrada", label: "Movimentações de Entrada" },
              { value: "movimentacoes_saida", label: "Movimentações de Saída" },
              { value: "movimentacoes_interna", label: "Movimentações Internas" }
            ]}
          />

          {/* Box pontilhada escrita "Arraste aqui os arquivos" */}
          <DragBox />

          {/* Botao 'procure nesse dispositivo" */}
          <Button sx={button_model}>
            Procurar nesse dispositivo
          </Button>


        </Stack>
        {/* Botoes cancelar e Enviar: Alinhar a direita */}
        <Stack spacing={2} direction={"row"} p={3}>
          <Button sx={cancel_button}>Cancelar</Button>
          <Button sx={accept_button}>Enviar</Button>
        </Stack>
      </Stack>
    </Paper>
  )
}

export default UploadDialog
