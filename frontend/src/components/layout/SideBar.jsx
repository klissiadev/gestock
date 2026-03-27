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
import HomeActiveSvg from "../../assets/icon/icon-home-purple.svg?react";
import ChatSvg from "../../assets/icon/iconChat.svg?react";
import ChatActiveSvg from "../../assets/icon/icon-minerva-purple.svg?react";
import InvetorySvg from "../../assets/icon/iconInventory.svg?react";
import InvetoryActiveSvg from "../../assets/icon/icon-box-purple.svg?react";
import ShoppingSvg from "../../assets/icon/iconShop.svg?react";
import ShoppingActiveSvg from "../../assets/icon/icon-car-purple.svg?react";
import ChartSvg from "../../assets/icon/iconBars.svg?react";
import ChartActiveSvg from "../../assets/icon/icon-charts-purple.svg?react";
import LogOutSvg from "../../assets/icon/iconOut.svg?react";
import MovSvg from "../../assets/icon/iconMove.svg?react";
import MovActiveSvg from "../../assets/icon/icon-movement-purple.svg?react";
import UploadSvg from "../../assets/icon/iconUpload.svg?react";
import TeamSvg from "../../assets/icon/iconTeam.svg?react";
import TeamActiveSvg from "../../assets/icon/icon-team-purple.svg?react";
import LogoSvg from "../../assets/icon/logo-icon.svg?react";
import LogoTextSvg from "../../assets/icon/logo-text-purple.svg?react";

import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ArchiveIcon from "../../assets/icon/iconFiles.svg?react";

import { useAuth } from "../../AuthContext";


const commonItems = [
  { id: "home", icon: HomeSvg, title: "Home", iconActive: HomeActiveSvg },
  { id: "ai", icon: ChatSvg, title: "Chat", iconActive: ChatActiveSvg},
  { id: "upload", icon: UploadSvg, title: "Upload", iconActive: UploadSvg },
  { id: "sheets", icon: InvetorySvg, title: "Inventory", iconActive: InvetoryActiveSvg },
  { id: "movements", icon: MovSvg, title: "Movements", iconActive: MovActiveSvg },
  { id: "requests", icon: ShoppingSvg, title: "Request", iconActive: ShoppingActiveSvg },
  { id: "forecast", icon: ChartSvg, title: "Forecast", iconActive: ChartActiveSvg}
];

const adminItems = [
  { id: "debug2", icon: HomeSvg, title: "Home", iconActive: HomeSvg },
  { id: "users", icon: TeamSvg, title: "Users", iconActive: TeamActiveSvg},
  { id: "log-imports", icon: ArchiveIcon, title: "Log Imports", iconActive: ArchiveIcon},
  { id: "log-chats", icon: ChatSvg, title: "Log Chats", iconActive: ChatActiveSvg}
];

export default function SideBar({ active, onChange, expanded, onToggle }) {
  const COLLAPSED_WIDTH = 66;
  const EXPANDED_WIDTH = 180; 
  const { logout, isAdmin } = useAuth();

  const menuItems = isAdmin
  ? adminItems
  : commonItems;

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
            backgroundColor: (theme) => theme.palette.primary.main,
            color: "#000",
            fontWeight: "bold",

            "&:hover": {
              backgroundColor: (theme) => theme.palette.iconButton.selected,
            },
          }}
        >
          {expanded ? <ChevronLeftIcon sx={{ color: "#fff" }} /> : <ChevronRightIcon sx={{ color: "#fff" }} />}
        </IconButton>
      </Box>


       {/* Logo */}
      <Box display="flex" justifyContent="center">
        <IconButton sx={{width:expanded ? "120px":"34px"}}>
          {expanded ? <LogoTextSvg/> : <LogoSvg sx={{ color: "#fff" }}/>}
        </IconButton>
      </Box>

      <Divider sx={{ mt: 1, mb: 1, borderWidth: 1.3}} />

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
                <AppIcon component={active === item.id ? item.iconActive : item.icon} />
              </ListItemIcon>

              {expanded && (
                <ListItemText
                  primary={item.title}
                  sx={{ 
                    whiteSpace: "nowrap",
                    maxWidth: expanded ? "100%" : 0,
                    transition: "opacity 0.2s",
                    color: (theme) => active === item.id ? theme.palette.primary.main : "#000"
                  }}
                />
              )}
            </ListItemButton>
          );

          return expanded ? (
            <Box key={item.id}>{button}</Box>
          ) : (
            <Tooltip key={item.id}  title={item.title} placement="right">
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

