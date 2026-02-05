import { Stack, Divider, Typography, Button, CircularProgress } from "@mui/material";
import { stack_principal } from "./styles/style";
import UploadDialog from "./pages/UploadDialog";
import { useFileUpload } from "./hooks/useFileManager";
import CloudDownloadRoundedIcon from "@mui/icons-material/CloudDownloadRounded";

const UploadPageDebug = () => {
  const testDownload = async () => {
    try {
      // 1. Faz a requisição para o seu backend
      const response = await fetch(
        "http://localhost:8000/views/download/transaction",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          // Envie um filtro vazio ou um objeto padrão para o teste
          body: JSON.stringify({
            searchTerm: "",
            orderBy: "id",
            isAsc: true,
            categoria: "",
            isBaixoEstoque: false,
            isVencidos: false,
          }),
        },
      );

      if (!response.ok) throw new Error("Erro no servidor");

      // 2. Transforma a resposta em um BLOB (Binary Large Object)
      const blob = await response.blob();

      // 3. Cria uma URL temporária para esse arquivo na memória do navegador
      const url = window.URL.createObjectURL(blob);

      // 4. Cria um elemento "<a>" invisível para forçar o download
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "teste_relatorio.xlsx"); // Nome do arquivo

      // 5. Simula o clique e depois remove o elemento
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

      // 6. Limpa a memória
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Falha no download:", error);
      alert("Erro ao baixar o PDF. Verifique o console.");
    }
  };

  const teste = () => {
    alert("Botao");
  };
  return (
    <Stack
      direction="column"
      spacing={2}
      alignItems="center"
      sx={stack_principal}
    >
      <Button
        size="large"
        onClick={teste}
        variant="outlined" // Já resolve borda e estilo básico
        startIcon={<CloudDownloadRoundedIcon />}
        sx={{
          color: theme => theme.palette.common.black,
          borderColor: theme => theme.palette.common.black,
          borderRadius: 2,
          textTransform: "none", // Mantém o texto como você digitou (sem Caps Lock)
          "&:hover": {
            borderColor: theme => theme.palette.common.black,
            backgroundColor: theme => theme.palette.table.main,
          },
          // Faz o botão se ajustar ao conteúdo
          width: "fit-content",
          minWidth: "auto",
        }}
      >
        Download
      </Button>
    </Stack>
  );
};

export default UploadPageDebug;
