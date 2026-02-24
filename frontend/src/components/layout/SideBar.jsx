//src\components\layout\SideBar.jsx
import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Divider,
  Tooltip,
  IconButton
} from "@mui/material";

import AppIcon from "../ui/AppIcon";

import HomeSvg from "../../assets/icon/iconHome.svg?react";
import ChatSvg from "../../assets/icon/iconChat.svg?react";
import InvetorySvg from "../../assets/icon/iconInventory.svg?react";
import ShoppingSvg from "../../assets/icon/iconShop.svg?react";
import ChartSvg from "../../assets/icon/iconBars.svg?react";
import ReportsSvg from "../../assets/icon/iconRecord.svg?react";
import LogOutSvg from "../../assets/icon/iconOut.svg?react";
import MovSvg from "../../assets/icon/iconMove.svg?react";
import UploadSvg from "../../assets/icon/iconUpload.svg?react";

import MonitorHeartOutlinedIcon from '@mui/icons-material/MonitorHeartOutlined';
import AddCircleOutlineOutlinedIcon from '@mui/icons-material/AddCircleOutlineOutlined';
import ManageAccountsOutlinedIcon from '@mui/icons-material/ManageAccountsOutlined';
import AutoAwesomeOutlinedIcon from '@mui/icons-material/AutoAwesomeOutlined';
import ImportExportOutlinedIcon from '@mui/icons-material/ImportExportOutlined';

import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";

import { useAuth } from "../../AuthContext";


const GestorMenuItems = [
  { id: "home", icon: HomeSvg, title: "Home" },
  { id: "ai", icon: ChatSvg, title: "Chat" },
  { id: "upload", icon: UploadSvg, title: "Upload" },
  { id: "sheets", icon: InvetorySvg, title: "Inventory" },
  { id: "movements", icon: MovSvg, title: "Movements" },
  { id: "requests", icon: ShoppingSvg, title: "Request" },
  { id: "forecast", icon: ChartSvg, title: "Forecast" },
  { id: "reports", icon: ReportsSvg, title: "Reports" },
];

const adminMenuItems = [
  { id: "health", icon: MonitorHeartOutlinedIcon, title: "Saúde do Sistema" },
  { id: "add-user", icon: AddCircleOutlineOutlinedIcon, title: "Adicionar Usuário" },
  { id: "manage-users", icon: ManageAccountsOutlinedIcon, title: "Gerenciar Usuários" },
  { id: "minerva-log", icon: AutoAwesomeOutlinedIcon, title: "Log de Minerva" },
  { id: "import-log", icon: ImportExportOutlinedIcon, title: "Log de Importação" },
]

export default function SideBar({ active, onChange, expanded, onToggle, isAdmin = false }) {
  const COLLAPSED_WIDTH = 66;
  const EXPANDED_WIDTH = isAdmin ? 230 : 180 ;
  const { logout } = useAuth();

  const menuItems = isAdmin ? adminMenuItems : GestorMenuItems;

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: expanded ? EXPANDED_WIDTH : COLLAPSED_WIDTH,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          ml: 2,
          mt: 2,
          width: expanded ? EXPANDED_WIDTH : COLLAPSED_WIDTH,
          overflow: "visible",
          position: "relative",

          display: "flex",
          flexDirection: "column",
        },
      }}
    >

      <Box
        sx={{
          position: "absolute",
          top: 80,
          right: -14,
          zIndex: 1600,
        }}
      >
        <IconButton
          onClick={onToggle}
          sx={{
            width: 25,
            height: 25,
            borderRadius: '8px',
            backgroundColor: "#DBDBDB",
            color: "#000",
            fontWeight: "bold",

            "&:hover": {
              backgroundColor: "#f5f5f5",
            },
          }}
        >
          {expanded ? <ChevronLeftIcon /> : <ChevronRightIcon />}
        </IconButton>
      </Box>


      {/* Logo */}
      <Box display="flex" justifyContent="center">
        <IconButton>
          <img src="/logo.svg" width={28} />
        </IconButton>
      </Box>

      <Divider sx={{ mt: 2, mb: 1, borderWidth: 1.3 }} />

      {/* Menu */}
      <Box sx={{ flex: 1 }}>
        <List sx={{ px: 1, mt: 3 }}>
          {menuItems.map((item) => {
            const button = (
              <ListItemButton
                key={item.id}
                selected={active === item.id}
                onClick={() => onChange(item.id)}
                sx={{
                  justifyContent: expanded ? "left" : "center",
                  gap: 1,
                  width: expanded ? "100%" : "80%",
                  minHeight: 40,
                  px: expanded ? 1.4 : 2.4,
                  py: 0.8,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: expanded ? 1 : 0,
                    justifyContent: "center",
                  }}
                >
                  <AppIcon component={item.icon} />
                </ListItemIcon>

                {expanded && (
                  <ListItemText
                    primary={item.title}
                    sx={{
                      whiteSpace: "nowrap",
                      maxWidth: expanded ? "100%" : 0,
                      transition: "opacity 0.2s",
                    }}
                  />
                )}
              </ListItemButton>
            );

            return expanded ? (
              <Box key={item.id}>{button}</Box>
            ) : (
              <Tooltip key={item.id} title={item.title} placement="right">
                {button}
              </Tooltip>
            );
          })}
        </List>
      </Box>

      {/* Logout */}
      <Box display="flex" justifyContent="center" mt={2} px={1}>
        <ListItemButton
          sx={{
            justifyContent: expanded ? "left" : "center",
            gap: 1,
            width: expanded ? "100%" : "80%",
            minHeight: 40,
            px: expanded ? 1.4 : 2.4,
            py: 0.8,
          }}
          onClick={() => logout()}
        >
          <ListItemIcon
            sx={{
              minWidth: 0,
              mr: expanded ? 1 : 0,
              justifyContent: "center",
            }}
          >
            <AppIcon component={LogOutSvg} />
          </ListItemIcon>

          {expanded && (
            <ListItemText
              primary="Logout"
              sx={{
                whiteSpace: "nowrap",
                maxWidth: expanded ? "100%" : 0,
                transition: "opacity 0.2s",
              }}
            />
          )}
        </ListItemButton>
      </Box>
    </Drawer>
  );
}

