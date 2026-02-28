import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  IconButton,
} from "@mui/material";

const CustomTable = ({ columns, rows, actions }) => {
  return (
    <TableContainer sx={{ flex:1, overflowY: "auto", borderRadius: 3 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {columns.map((col) => (
              <TableCell key={col.field}>
                {col.header}
              </TableCell>
            ))}

            {actions && <TableCell>Ações</TableCell>}
          </TableRow>
        </TableHead>

        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              {columns.map((col) => (
                <TableCell key={col.field}>
                  {col.render
                    ? col.render(row)
                    : row[col.field]}
                </TableCell>
              ))}

              {actions && (
                <TableCell>
                  <Box display="flex" justifyContent="center">
                    {actions.map((action, index) => (
                      <IconButton
                        key={index}
                        size="small"
                        onClick={() => action.onClick(row)}
                      >
                        {action.icon}
                      </IconButton>
                    ))}
                  </Box>
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CustomTable;