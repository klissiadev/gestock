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

import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";


const menuItems = [
  { id: "home", icon: HomeSvg, title: "Home" },
  { id: "ai", icon: ChatSvg, title: "Chat"},
  { id: "sheets", icon: InvetorySvg, title: "Inventory" },
  { id: "requests", icon: ShoppingSvg, title: "Request" },
  { id: "forecast", icon: ChartSvg, title: "Forecast"},
  { id: "reports", icon: ReportsSvg, title: "Reports" },
];

export default function SideBar({ active, onChange, expanded, onToggle }) {
  const COLLAPSED_WIDTH = 66;
  const EXPANDED_WIDTH = 180;

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

          transition: (theme) =>
            theme.transitions.create("width", {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.standard,
            }),
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

      <Divider sx={{ mt: 2, mb: 3, borderWidth: 1.3}} />

      {/* Menu */}

      <List 
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          pb: 16,
          gap: 0.5
        }}
      >
        {menuItems.map((item) => {
          const button = (
            <ListItemButton
              selected={active === item.id}
              onClick={() => onChange(item.id)}
              sx={{
                justifyContent: expanded ? "space-between" : "center",
                gap: 1,
                width: expanded ? "100%" : "80%"
              }}
            >
              <ListItemIcon>
                <AppIcon component={item.icon} />
              </ListItemIcon>

              {expanded && (
                <ListItemText
                  primary={item.title}
                  sx={{ 
                    whiteSpace: "nowrap",
                    maxWidth: expanded ? "100%" : 0,
                    transition: "opacity 0.2s",
                    whiteSpace: "nowrap",
                  }}
                />
              )}
            </ListItemButton>
          );

          return expanded ? (
            button
          ) : (
            <Tooltip title={item.title} placement="right">
              {button}
            </Tooltip>
          );
        })}
      </List>

      {/* Logout */}
      <Box display="flex" justifyContent="center" mt={2} >
        <IconButton>
          <AppIcon component={LogOutSvg} />
        </IconButton>
      </Box>
    </Drawer>
  );
}

