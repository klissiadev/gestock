import React from 'react'
import { Box, Typography } from "@mui/material";
import ChartSvg from "../../../assets/icon/iconChart.svg?react"; 

const CardStock = ({ title, value, percentage, period }) => {
  return (
    <Box 
        sx={(theme) => ({
            px: 4, 
            py: 1,
            width: "100%",
            textAlign: "center",
            backgroundColor: theme.palette.card.background,
            borderRadius: 3,
        })}
    >  
        <Typography fontSize={16} >
            {title}
        </Typography>

        <Typography variant="h4" sx={{ mt: 2 }}>
            {value}
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", mt: 1 , gap: 1}}>
            <ChartSvg width={14} height={16} />
            <Typography  fontSize={14}>
                {percentage}% que o {period} passado
            </Typography>
        </Box>
    </Box>
  )
}

export default CardStock