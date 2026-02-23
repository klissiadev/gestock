import React from 'react'
import { Box, Typography } from '@mui/material'
import { dragBox, uploadText } from '../styles/style'
import { useDropzone } from 'react-dropzone';

const DragBox = ({ onFileSelect }) => {

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop: (acceptedFiles) => {
            if (acceptedFiles.length > 0) {
                onFileSelect(acceptedFiles[0]);
            }
        },
        accept: {
            'text/csv': ['.csv'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
        },
        multiple: false,
    });



    return (
        <Box {...getRootProps()} sx={{
            ...dragBox, cursor: 'pointer',
            transition: 'all 0.2s ease',
            borderColor: (theme) => isDragActive ? theme.palette.primary.main : theme.palette.button.main,
            backgroundColor: (theme) => isDragActive ? theme.palette.action.hover : "transparent",
        }}>
            <input {...getInputProps()} />
            <Typography sx={{
                ...uploadText,
                color: isDragActive ? 'primary.main' : 'text.primary'
            }}>
                {isDragActive ? "Solte o arquivo aqui..." : "Arraste seus arquivos aqui"}
            </Typography>
        </Box>
    )
}

export default DragBox
