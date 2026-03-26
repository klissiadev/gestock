import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  IconButton,
  Skeleton,
  Typography,
} from "@mui/material";
import InboxIcon from "@mui/icons-material/Inbox";


const TableLoadingState = ({ colSpan }) => (
  <>
    {Array.from(new Array(5)).map((_, index) => (
      <TableRow key={`skeleton-${index}`}>
        {Array.from(new Array(colSpan)).map((_, colIndex) => (
          <TableCell key={colIndex}>
            <Skeleton variant="text" height={30} animation="wave" />
          </TableCell>
        ))}
      </TableRow>
    ))}
  </>
);

const TableEmptyState = ({ colSpan, message }) => (
  <TableRow>
    <TableCell colSpan={colSpan} sx={{ py: 10 }}>
      <Box display="flex" flexDirection="column" alignItems="center" gap={1} sx={{ opacity: 0.4 }}>
        <InboxIcon sx={{ fontSize: 48 }} />
        <Typography variant="body1" fontWeight={500}>{message}</Typography>
      </Box>
    </TableCell>
  </TableRow>
);



const CustomTable = ({ columns, rows, actions, loading, emptyMessage = "Nenhum registro encontrado" }) => {

  const totalColumns = columns.length + (actions ? 1 : 0);

  const renderTableContent = () => {
    if (loading) {
      return <TableLoadingState colSpan={totalColumns} />;
    }

    if (rows.length === 0) {
      return <TableEmptyState colSpan={totalColumns} message={emptyMessage} />;
    }

    return rows.map((row) => (
      <TableRow key={row.id} hover>
        {columns.map((col) => (
          <TableCell key={col.field}>
            {col.render ? col.render(row) : row[col.field]}
          </TableCell>
        ))}

        {actions && (
          <TableCell>
            <Box display="flex" justifyContent="center" gap={1}>
              {actions.map((action, index) => (
                <IconButton
                  key={index}
                  size="small"
                  onClick={() => action.onClick(row)}
                  sx={{ color: action.color || 'inherit' }}
                >
                  {action.icon}
                </IconButton>
              ))}
            </Box>
          </TableCell>
        )}
      </TableRow>
    ));

  }

  return (
    <TableContainer sx={{ flex: 1, overflow: 'auto', borderRadius: '8px' }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {columns.map((col) => (
              <TableCell key={col.field} sx={{ width: col.width || 'auto', fontWeight: 'bold', bgcolor: 'background.paper' }}>
                {col.header}
              </TableCell>
            ))}
            {actions && <TableCell align="center" sx={{ fontWeight: 'bold', bgcolor: 'background.paper' }}>Ações</TableCell>}
          </TableRow>
        </TableHead>

        <TableBody>
          {renderTableContent()}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CustomTable;