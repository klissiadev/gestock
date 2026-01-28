import SideBar from "../../components/layout/SideBar";
import { useState } from "react";
import { Box } from "@mui/material";
import { ToastContainer } from "react-toastify";

export default function HomePage() {
  const [active, setActive] = useState("home");

  return (
    <Box>
      <ToastContainer />
    <SideBar active={active} onChange={setActive} />
    </Box>
  );
}

