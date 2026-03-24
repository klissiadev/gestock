import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography, Box
} from "@mui/material";

const ReportTable = ({ reportType, payload, metadata }) => {
  const registros = payload.dados || [];
  const titulo = reportType.replace(/_/g, ' ').toUpperCase();

  return (
    <Box sx={{ width: '100%', my: 1 }}>
      <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1, color: 'primary.main' }}>
        {titulo}
      </Typography>

      <TableContainer component={Paper} variant="outlined" sx={{ maxHeight: 400 }}>
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow>
              <TableCell sx={{ bgcolor: 'action.hover', fontWeight: 600 }}>Registros do Sistema</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {registros.map((item, index) => (
              <TableRow key={index} hover>
                <TableCell sx={{
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'monospace',
                  fontSize: '0.85rem',
                  verticalAlign: 'top'
                }}>
                  {item}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1, opacity: 0.8 }}>
        <Typography variant="caption">Total: {payload.total_items} itens</Typography>
        {metadata?.valor_total_estoque && (
          <Typography variant="caption" sx={{ fontWeight: 600 }}>
            Valor Total: {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(metadata.valor_total_estoque)}
          </Typography>
        )}
      </Box>
    </Box>
  );
};

export default ReportTable;