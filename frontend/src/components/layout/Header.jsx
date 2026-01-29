import React from 'react'
import { Box, IconButton, Button, Typography} from "@mui/material";
import AppIcon from "../ui/AppIcon";
import PerfilSvg from "../../assets/icon/iconPerfil.svg?react";
import NotificationSvg from "../../assets/icon/iconNotify.svg?react";
import AddSvg from "../../assets/icon/iconAdd.svg?react";

const Header = () => {
    const nome = "Carlos Ribeiro";
    return (
        <Box 
            sx={{
                bgcolor: 'background.paper',
                borderRadius: 3,
                p: 1,
                ml: 2.5  ,
                display: "flex",
                flex: 1,
                alignItems:"center",
                justifyContent:"space-between"
            }}
        >
            <Box display="flex" alignItems="center" justifyContent="space-between" gap={2} ml={1}>
                <IconButton
                    sx={{
                        borderRadius: '12px',
                        border: '1.5px solid',
                        borderColor: 'common.black'
                    }}
                >
                    <PerfilSvg width={18} height={18}/>
                </IconButton>
                <Typography fontSize={18} >{nome}</Typography>
            </Box>
            <Box display="flex" alignItems="center" justifyContent="space-between" gap={2} mr={1}>
                <Button 
                    variant="contained" 
                    color="primary" 
                    startIcon={<AddSvg width={18} height={18} />}
                    sx={{ 
                        textTransform: 'none', 
                        borderRadius: '12px', 
                        border: '1.5px solid',    
                        borderColor: 'common.black',
                        fontSize: 14
                }}
                > Nova requisição</Button>
                <IconButton
                    sx={{
                        borderRadius: '12px',
                        border: '1.5px solid',
                        borderColor: 'common.black'
                    }}
                >
                    <NotificationSvg width={18} height={18}/>
                </IconButton>
            </Box>
        </Box>
    )
}

export default Header