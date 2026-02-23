import {
  TableRow,
  TableCell,
  Skeleton,
  TableContainer,
  Table,
  TableBody,
  Box,
} from "@mui/material";

const LoadingComponent = ({ columns, rowsPerPage = 12 }) => {
  return (
    <TableContainer>
      <Table>
        <TableBody>
          {[...Array(rowsPerPage)].map((_, rowIndex) => (
            <TableRow key={rowIndex}>
              {columns.map((col, colIndex) => (
                <TableCell key={colIndex}>
                  <Box sx={{ display: "flex", justifyContent: "center" }}>
                    <Skeleton
                      variant="text"
                      animation="wave"
                      width="80%"
                      height={30}
                    />
                  </Box>
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default LoadingComponent;
