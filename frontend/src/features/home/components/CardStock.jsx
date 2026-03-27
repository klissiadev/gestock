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
            backgroundColor: theme.palette.primary.main,
            borderRadius: 3,
            pt:2,
            boxShadow: "0 4px 20px rgba(0,0,0,0.16)",
            color: theme.palette.common.white
        })}
    >  
        <Typography fontSize={18} >
            {title}
        </Typography>

        <Typography variant="h4" sx={{ mt: 1 }}>
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