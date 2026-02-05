import{ useState } from "react";
import { FormControl, Button, CircularProgress } from "@mui/material";
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
          color: (theme) => theme.palette.common.black,
          borderColor: (theme) => theme.palette.common.black,
          borderRadius: 2,
          padding: 2,
          textTransform: "none",
          "&:hover": {
            borderColor: (theme) => theme.palette.common.black,
            backgroundColor: (theme) => theme.palette.table.main,
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
