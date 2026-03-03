import React from "react";
import { Box, IconButton, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import PerfilSvg from "../../assets/icon/iconPerfil.svg?react";
import NotificationSvg from "../../assets/icon/iconNotify.svg?react";
import AddUserSvg from "../../assets/icon/iconAddUser.svg?react";
import AddSvg from "../../assets/icon/iconAdd.svg?react";

import PeriodSelector from "../ui/PeriodSelector";
import { useHeader } from "../../HeaderContext";
import { useAuth } from "../../AuthContext";

const Header = () => {
  const { user } = useAuth();
  const { headerConfig } = useHeader();
  const navigate = useNavigate();

  const nome = user?.nome ?? "";

  const getActionButton = () => {
    switch (headerConfig.variant) {
      case "home":
        return (
          <PeriodSelector
            value={headerConfig.period}
            onChange={headerConfig.onPeriodChange}
          />
        );

      case "users":
        return (
          <Button
            variant="contained"
            startIcon={<AddUserSvg width={18} height={18} />}
            sx={buttonStyle}
            onClick={() => navigate("/register-user")}
          >
            Adicionar usuário
          </Button>
        );

      default:
        return (
          <></>
        );
    }
  };

  return (
    <Box sx={containerStyle}>
      {/* Perfil */}
      <Box display="flex" alignItems="center" gap={2} ml={1}>
        <IconButton sx={iconStyle}>
          <PerfilSvg width={18} height={18} />
        </IconButton>
        <Typography fontSize={18}>{nome}</Typography>
      </Box>

      {/* Ações */}
      <Box display="flex" alignItems="center" gap={2} mr={1}>
        {getActionButton()}

        <IconButton sx={iconStyle}>
          <NotificationSvg width={18} height={18} />
        </IconButton>
      </Box>
    </Box>
  );
};

const containerStyle = {
  bgcolor: "background.paper",
  borderRadius: 3,
  p: 1,
  ml: 2.5,
  display: "flex",
  flex: 1,
  alignItems: "center",
  justifyContent: "space-between",
};

const iconStyle = {
  borderRadius: "12px",
  border: "1.5px solid",
  borderColor: "common.black",
};

const buttonStyle = {
  textTransform: "none",
  borderRadius: "12px",
  border: "1.5px solid",
  borderColor: "common.black",
  fontSize: 14,
};

export default Header;