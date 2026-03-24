import React from 'react'
import { Box, Typography, Stack, Divider} from "@mui/material";
import ExpandableIconButton from "../../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../../assets/icon/iconChat.svg?react";
import AddUserSvg from "../../../assets/icon/iconAddUser.svg?react";

const RegisterUserBar = ({titulo}) => {
  return (
    <Stack x={1}>
      <Stack direction="row" alignItems="center" pb={2}>
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 1,
          }}
        >
          <AddUserSvg width={18} height={18} />
          <Typography fontSize={20} fontWeight={500}>
            {titulo}
          </Typography>
        </Box>
      </Stack>
      <Divider variant="middle" />  
    </Stack>
  )
}

export default RegisterUserBar