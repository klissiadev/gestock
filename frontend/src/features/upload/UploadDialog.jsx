import { useRef, useState, useEffect } from 'react';
import { Paper, Stack, Typography, Divider, Button, CircularProgress } from '@mui/material'
import TypeSelector from "./components/TypeSelector";
import DragBox from "./components/DragBox";
import { button_model, cancel_button, accept_button, paper_box, uploadText } from "./styles/style";
import { useFileUpload } from './hooks/useFileManager';
import SucessBox from './components/SucessBox';

const UploadDialog = () => {
  const {
    fileName, tipo, loading, error, response,
    onFileChange, onDropSelect, handleTypeChange, executeUpload, clear
  } = useFileUpload();

  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    console.log("Response foi: ", response)
    if (response && response.log && response.log.status === "SUCESSO") {
      setShowSuccess(true);
    }
  }, [response]);

  const handleCloseSuccess = () => {
    setShowSuccess(false);
    clear(); // Limpa o formulário de upload ao fechar
  };

  // Referência para o input escondido
  const fileInputRef = useRef(null);

  const handleBrowseClick = () => {
    fileInputRef.current.click();
  };

  return (
    <Paper
      elevation={1}
      sx={paper_box}
    >
      {/* Input de arquivos escondido */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={onFileChange}
        style={{ display: 'none' }}
        accept=".csv, .xlsx"
      />

      <Stack direction="column" spacing={2}>
        {error && <Typography color="error">{error}</Typography>}
        <Typography variant="h6" sx={uploadText}>
          Anexar Arquivos
        </Typography>

        <Divider />

        {/* Aqui entra a dropzone */}
        <Stack direction="column" spacing={2} alignItems="center">
          <Typography sx={uploadText}>
            Envie seus arquivos .csv ou .xlsx
          </Typography>

          {/* Select Tipo do arquivo */}
          <TypeSelector
            name="sheet_selector"
            value={tipo}
            onChange={(value) => handleTypeChange(value)}
            placeholder="Todas as Categorias"
            options={[
              { value: "produtos", label: "Produtos" },
              { value: "movimentacoes_entrada", label: "Movimentações de Entrada" },
              { value: "movimentacoes_saida", label: "Movimentações de Saída" },
              { value: "movimentacoes_interna", label: "Movimentações Internas" }
            ]}
          />

          <DragBox onFileSelect={onDropSelect} />

          <Button sx={button_model} onClick={handleBrowseClick}>
            Procurar nesse dispositivo
          </Button>

          {/* Mostra o nome do arquivo selecionado */}
          <Typography variant="caption" sx={{ mt: 1, color: 'text.secondary' }}>
            {fileName}
          </Typography>


        </Stack>
        {/* Botoes cancelar e Enviar: Alinhar a direita */}
        <Stack spacing={2} direction={"row"} p={3}>
          <Button sx={cancel_button} onClick={clear} disabled={loading}>Cancelar</Button>
          <Button sx={accept_button}
            onClick={executeUpload}
            disabled={loading || fileName === "Nenhum arquivo selecionado"}>

            {loading ? <CircularProgress size={24} color="inherit" /> : "Enviar"}
          </Button>


        </Stack>
        <SucessBox
          open={showSuccess}
          handleClose={handleCloseSuccess}
        />
      </Stack>
    </Paper >
  )
}

export default UploadDialog
