import React from 'react'
import { Box, Typography, Stack, Divider} from "@mui/material";
import ExpandableIconButton from "../../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../../assets/icon/iconChat.svg?react";
import AddUserSvg from "../../../assets/icon/iconAddUser.svg?react";

const RegisterUserBar = ({titulo}) => {
  return (
    <Stack x={1}>
      <Stack direction="row" alignItems="center" pb={1}>
        <Box sx={{ flex: 1 }} />

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

        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <ExpandableIconButton
            icon={<ChatSvg width={16} height={16} />}
            origin="register-user"
            initialMessage="Olá Minerva, me ajude em como adicionar novo usuário."
          />
        </Box>
      </Stack>
      <Divider variant="middle" />  
    </Stack>
  )
}

export default RegisterUserBar