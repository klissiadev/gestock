import React from 'react'
import { Box, Typography } from '@mui/material'
import { dragBox, uploadText } from '../styles/style'

const DragBox = () => {
    return (
        <Box sx={dragBox}>
            <Typography sx={uploadText}>
                Arraste seus arquivos aqui
            </Typography>
        </Box>
    )
}

export default DragBox
