import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { Box } from "@mui/material";
import { ToastContainer } from "react-toastify";
import { useState } from "react";

import SideBar from "./SideBar";
import PageContainer from "./PageContainer";
import Header from "./Header";


export default function AppLayout() {
    const location = useLocation();
    const navigate = useNavigate();
    const [expanded, setExpanded] = useState(false);

    // rota atual => sidebar ativa
    const active = location.pathname.replace("/", "") || "home";

    /**
     * @param {string} route
     */

    function handleChange(route) {
        navigate(route === "home" ? "/" : `/${route}`);
    }

    function toggleSidebar() {
        setExpanded((prev) => !prev);
    }

    return (
        <Box display="flex" minHeight="100vh">
            <ToastContainer />
            <SideBar 
                active={active}
                onChange={handleChange}
                expanded={expanded}
                onToggle={toggleSidebar}
            />
            
            {/* Conteúdo da página */}
            <Box flex={1} p={2} >
                <Header />
                <PageContainer>
                    <Outlet />
                </PageContainer>
            </Box>
        </Box>
    );
}
