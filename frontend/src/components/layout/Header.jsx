import { Box, IconButton, Button, Typography, Badge } from "@mui/material";
import { useNavigate } from "react-router-dom";
import {  } from "@mui/material";
import { useEffect, useState } from "react";
import { fetchUnreadNotifications } from "../../features/notifications/services/notificationApi";
import PerfilSvg from "../../assets/icon/iconPerfil.svg?react";
import NotificationSvg from "../../assets/icon/iconNotify.svg?react";
import AddUserSvg from "../../assets/icon/iconAddUser.svg?react";
import HistoryIcon from "@mui/icons-material/History";

import PeriodSelector from "../ui/PeriodSelector";
import { useHeader } from "../../HeaderContext";
import { useAuth } from "../../AuthContext";

const Header = () => {
  const { user } = useAuth();
  const { headerConfig } = useHeader();
  const navigate = useNavigate();

  const nome = user?.nome ?? "";

  const [hasUnread, setHasUnread] = useState(false);

  useEffect(() => {
    async function checkUnread() {
      try {
        const data = await fetchUnreadNotifications(1);
        setHasUnread(data.length > 0);
      } catch (err) {
        console.error(err);
      }
    }

    checkUnread();

    const interval = setInterval(checkUnread, 30000);

    return () => clearInterval(interval);
  }, []);

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

      case "requests":
        return (
          <Button
            variant="contained"
            startIcon={<HistoryIcon width={18} height={18} />}
            sx={buttonStyle}
            onClick={() => navigate("/history-requests")}
          >
            Ver requisições
          </Button>
        );

      default:
        return <></>;
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

        <IconButton
          sx={iconStyle}
          onClick={() => {
            navigate("/notifications");
            setHasUnread(false);
          }}
        >
          <Badge
            color="error"
            variant="dot"
            invisible={!hasUnread}
          >
            <NotificationSvg width={18} height={18} />
          </Badge>
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