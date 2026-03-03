import React from 'react'
import { Typography } from '@mui/material'

const ValidationLabel = ({ label, isValid }) => {
  return (
    <Typography
      variant="caption"
      display="block"
      sx={{
        textDecoration: isValid ? "none" : "line-through",
        color: isValid ? "green" : "error.main",
        transition: "all 0.3s ease"
      }}
    >
      {label}
    </Typography>
  )
}

export default ValidationLabel