import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { Box } from "@mui/material";
import { ToastContainer } from "react-toastify";

import SideBar from "./SideBar";
import PageContainer from "./PageContainer";
import Header from "./Header";


export default function AppLayout() {
    const location = useLocation();
    const navigate = useNavigate();

    // rota atual => sidebar ativa
    const active = location.pathname.replace("/", "") || "home";

    /**
     * @param {string} route
     */

    function handleChange(route) {
        navigate(route === "home" ? "/" : `/${route}`);
    }

    return (
        <Box display="flex" minHeight="100vh">
            <ToastContainer />
            <SideBar active={active} onChange={handleChange} />
            
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
