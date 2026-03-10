import { Box, TextField, Typography, Button } from "@mui/material";

const RequestForm = ({ products }) => {

  return (
    <Box
      sx={{
        p: 2,
        borderTop: "1px solid",
        borderColor: "divider",
        display: "flex",
        flexDirection: "column",
        gap: 2,
        alignItems:"center"
      }}
    >

      <TextField
        size="small"
        placeholder="Título"
        fullWidth
      />

      <TextField
        placeholder="Observações"
        multiline
        minRows={1}
        maxRows={6}
        />

      <Typography fontSize={12} color="text.secondary" textAlign={"center"}>
        {products.length} produtos foram adicionados
      </Typography>

      <Button
        variant="contained"
        fullWidth
        sx={{
            borderRadius: "12px",
            textTransform: "none",
            flex: 1,
            height: 40,
            fontFamily: (theme) => theme.typography.fontFamily,
            fontWeight: (theme) => theme.typography.fontWeightLight,
            color: theme => theme.palette.common.white,
            backgroundColor: (theme) => theme.palette.uploadBox.button,
            "&:hover": {
                backgroundColor: (theme) => theme.palette.button.hover,
                color: theme => theme.palette.common.black,
            },
        }}
      >
        Enviar
      </Button>

    </Box>
  );
};

export default RequestForm;