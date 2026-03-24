import{ useState } from "react";
import { Button, CircularProgress } from "@mui/material";
import {
  downloadProduct,
  downloadTransactions,
} from "../services/exportService";
import CloudDownloadRoundedIcon from "@mui/icons-material/CloudDownloadRounded";

const DownloadButton = ({ filter, whatTable }) => {
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);

  const config = {
    products: {
      action: downloadProduct,
    },
    transactions: {
      action: downloadTransactions,
    },
  };

  const currentConfig = config[whatTable] || { label: "Download", action: () => {} };

  const handleDownload = async () => {
    setLoading(true);
    setErro(null);

    try {
      await currentConfig.action(filter);
    } catch (err) {
      setErro("Falha ao baixar arquivo. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
      <Button
        size="large"
        onClick={handleDownload}
        variant="outlined"
        startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <CloudDownloadRoundedIcon />}
        sx={{
          color: (theme) => theme.palette.iconButton.hover,
          backgroundColor: (theme) => theme.palette.primary.main,
          borderRadius: 2,
          padding: 2,
          textTransform: "none",
          "&:hover": {
            backgroundColor: (theme) => theme.palette.iconButton.selected,
          },
          width: "fit-content",
          minWidth: "auto",
        }}
      >
        {loading ? "Processando..." : "Download"}
      </Button>
  );
};

export default DownloadButton;
