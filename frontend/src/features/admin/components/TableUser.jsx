import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  Avatar,
  IconButton,
} from "@mui/material";

import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import EditSvg from "../../../assets/icon/iconEdit.svg?react";
import DeleteSvg from "../../../assets/icon/iconDelete.svg?react";

const TableUser = ({ rows, selectedId }) => {
  return (
    <TableContainer
      sx={{
        maxHeight: 500,
        overflowY: "auto",
        borderRadius: 3,
      }}
    >
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {["Funcionário", "Email", "Função" , "Ações"].map(
              (header) => (
                <TableCell
                  key={header}
                >
                  {header}
                </TableCell>
              )
            )}
          </TableRow>
        </TableHead>

        <TableBody sx={{fontSize:"20px"}}>
          {rows.map((row) => (
            <TableRow>
              {/* Funcionário */}
              <TableCell>                
                <Box display="flex" alignItems="center" gap={3}  justifyContent={'center'}>
                  <Avatar
                    sx={{
                      width: 36,
                      height: 36,
                      backgroundColor: "#EAEAEA",
                      color: "#555",
                    }}
                  >
                    <PersonOutlineIcon fontSize="small" />
                  </Avatar>

                  {row.nome}
                </Box>
              </TableCell>

              {/* Email */}
              <TableCell>{row.email}</TableCell>

              {/* Função */}
              <TableCell>{row.funcao}</TableCell>

              {/* Ações */}
              <TableCell>
                <Box display="flex" justifyContent={'center'}>
                  <IconButton size="small">
                    <EditSvg width={18} height={18}/>
                  </IconButton>

                  <IconButton size="small">
                    <DeleteSvg width={18} height={18} />
                  </IconButton>
                </Box>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default TableUser;