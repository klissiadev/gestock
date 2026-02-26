import { Paper, Typography, Button, Stack } from "@mui/material";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
import RefreshIcon from "@mui/icons-material/Refresh";
import { theme } from "../../../style/theme";

const ErrorState = ({ message, onRetry }) => {
  return (
    <Paper variant="errorContainer">
      <ErrorOutlineIcon
        sx={{
          fontSize: 60,
          color: (theme) => theme.palette.errors.icon,
          mb: 2,
        }}
      />

      <Typography variant="h5" sx={{ fontFamily: theme => theme.typography.fontFamily, fontWeight: theme => theme.typography.fontWeightBold, mb: 1 }}>
        Ops! Algo deu errado.
      </Typography>

      <Typography
        variant="body1"
        sx={{ fontFamily: theme => theme.typography.fontFamily, fontWeight: theme => theme.typography.fontWeightLight, mb: 3 }}
      >
        {message ||
          "Não conseguimos carregar os dados do estoque agora. Verifique sua conexão ou tente novamente."}
      </Typography>

      <Stack direction="row" spacing={2}>
        <Button
          startIcon={<RefreshIcon />}
          onClick={onRetry}
          sx={{
            padding: 3,
            fontFamily: theme => theme.typography.fontFamily, 
            fontWeight: theme => theme.typography.fontWeightLight,
            borderColor: theme => theme.palette.background.default,
            border: '1px solid'
          }}
        >
          Tentar Novamente
        </Button>
      </Stack>
    </Paper>
  );
};

export default ErrorState;
