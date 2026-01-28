import { Drawer, List, Box, IconButton } from "@mui/material";
import AppIcon from "../ui/AppIcon";

import HomeSvg from "../../assets/icon/iconHome.svg?react";
import ChatSvg from "../../assets/icon/iconChat.svg?react";
import InvetorySvg from "../../assets/icon/iconInventory.svg?react";
import ShoppingSvg from "../../assets/icon/iconShop.svg?react";
import ChartSvg from "../../assets/icon/iconBars.svg?react";
import RecordSvg from "../../assets/icon/iconRecord.svg?react";
import LogOutSvg from "../../assets/icon/iconOut.svg?react";

const menuItems = [
  { id: "home", icon: HomeSvg },
  { id: "ai", icon: ChatSvg },
  { id: "box", icon: InvetorySvg },
  { id: "cart", icon: ShoppingSvg },
  { id: "chart", icon: ChartSvg },
  { id: "record", icon: RecordSvg },
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
      <Box display="flex" justifyContent="center" mb={3}>
        <IconButton>
          <img src="/logo.svg" width={28} />
        </IconButton>
      </Box>

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
          <IconButton
            key={item.id}
            onClick={() => onChange(item.id)}
            className={active === item.id ? "Mui-selected" : ""}
            sx={{
              width: 36,
              height: 36,
              borderRadius: '8px',
              padding:0
            }}
          >
            <AppIcon component={item.icon} />
          </IconButton>
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
