import { Drawer, List, Box, IconButton, Divider, Tooltip} from "@mui/material";
import AppIcon from "../ui/AppIcon";

import HomeSvg from "../../assets/icon/iconHome.svg?react";
import ChatSvg from "../../assets/icon/iconChat.svg?react";
import InvetorySvg from "../../assets/icon/iconInventory.svg?react";
import ShoppingSvg from "../../assets/icon/iconShop.svg?react";
import ChartSvg from "../../assets/icon/iconBars.svg?react";
import ReportsSvg from "../../assets/icon/iconRecord.svg?react";
import LogOutSvg from "../../assets/icon/iconOut.svg?react";

const menuItems = [
  { id: "home", icon: HomeSvg },
  { id: "ai", icon: ChatSvg },
  { id: "sheets", icon: InvetorySvg },
  { id: "requests", icon: ShoppingSvg },
  { id: "forecast", icon: ChartSvg },
  { id: "reports", icon: ReportsSvg },
];

export default function SideBar({ active, onChange }) {
  return (
    <Drawer
      variant="permanent"
      sx={{
        "& .MuiDrawer-paper": {
          ml: 2,
          mt: 2,
        },
      }}
    >
      
      {/* Logo */}
      <Box display="flex" justifyContent="center">
        <IconButton>
          <img src="/logo.svg" width={28} />
        </IconButton>
      </Box>

      <Divider sx={{ mt: 3, mb: 8, borderWidth: 1.3}} />

      {/* Menu */}
      <List
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 1,
        }}
      >
        {menuItems.map((item) => (
          <Tooltip title={item.id} >
            <IconButton
              key={item.id}
              onClick={() => onChange(item.id)}
              className={active === item.id ? "Mui-selected" : ""}
              sx={{
                width: 40,
                height: 40,
                borderRadius: '8px',
                padding:0
              }}
            >
              <AppIcon component={item.icon} />
            </IconButton>
          </Tooltip>
        ))}
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
