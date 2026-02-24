import React from 'react'
import { Box, Typography } from '@mui/material';
import { Gauge } from '@mui/x-charts';

const UsageBox = ({ name, usage }) => {
    return (
        <Box>

            <Gauge 
                value={usage}
                valueMin={0}
                valueMax={100}
                startAngle={-90}
                endAngle={90}

                height={200}
                width={200}
            
                text={({ value }) => `${value}%`}
            />

            <Typography>
                {name}
            </Typography>

        </Box>
    )
}

export default UsageBox