// frontend\src\components\layout\AppLayout.jsx
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { Box } from "@mui/material";
import { ToastContainer } from "react-toastify";
import { useState } from "react";
import { HeaderProvider } from "../../HeaderContext";


import SideBar from "./SideBar";
import PageContainer from "./PageContainer";
import Header from "./Header";



export default function AppLayout(isAdmin = false) {
    const location = useLocation();
    const navigate = useNavigate();
    const [expanded, setExpanded] = useState(false);

    // rota atual => sidebar ativa
    const active = location.pathname.replace("/", "") || "home";

    /**
     * @param {string} route
     */

    function handleChange(route) {
        navigate(`/${route}`);
    }

    function toggleSidebar() {
        setExpanded((prev) => !prev);
    }

    return (
        <HeaderProvider>
            <Box display="flex" height="100vh" sx={{ overflow: "hidden" }}>
                <ToastContainer />
                <SideBar 
                    active={active}
                    onChange={handleChange}
                    expanded={expanded}
                    onToggle={toggleSidebar}
                    isAdmin={isAdmin}
                />
                
                {/* Conteúdo da página */}
                <Box
                    sx={{
                        flex: 1,
                        display: "flex",
                        flexDirection: "column",
                        minWidth: 0,
                        p: 2,
                    }}
                    >
                    {/* HEADER FIXO */}
                    <Box sx={{ flexShrink: 0 }}>
                        <Header />
                    </Box>

                    {/* CONTEÚDO QUE SOBRA */}
                    <Box
                        sx={{
                        flex: 1,
                        minHeight: 0,
                        display: "flex",
                        overflow: "hidden"
                        }}
                    >
                        <PageContainer>
                        <Outlet />
                        </PageContainer>
                    </Box>
                    </Box>
            </Box>
        </HeaderProvider>
    );
}
