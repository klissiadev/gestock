import React from 'react'
import { Box, Avatar } from '@mui/material'
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";

const UserCell = ( { nome }) => {
    return (
        <Box
            display="flex"
            justifyContent="center"
            width="100%"
        >
            <Box
                display="flex"
                alignItems="center"
                gap={2}
                sx={{ width: '200px', justifyContent: 'flex-start' }}
            >
                <Avatar
                    sx={{
                        width: 36,
                        height: 36,
                        backgroundColor: "#EAEAEA",
                        color: "#555",
                    }}
                >
                    <PersonOutlineIcon fontSize="small" />
                </Avatar>

                <Box component="span" sx={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {nome}
                </Box>
            </Box>
        </Box>
    )
}

export default UserCell