import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableFooter,
  Checkbox
} from "@mui/material";

const TableModel = ({ rows, columns }) => {
  return (
      <TableContainer>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={col.field}>
                  {col.headerName}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.id}>
                {columns.map((col) => (
                  <TableCell key={col.field}>
                    {typeof row[col.field] === "boolean" ? (
                      <Checkbox checked={row[col.field]} disabled />
                    ) : (
                      row[col.field]
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
          <TableFooter>
            {/* Por enquanto sem sistema de paginação */}
          </TableFooter>
        </Table>
      </TableContainer>
  );
};

export default TableModel;
