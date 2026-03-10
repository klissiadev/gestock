import { Box, Paper, Typography, Stack } from '@mui/material'
import ArcGauge from './ArcGauge'

const SystemDashboard = ({ cpu_usage = 25.5, ram_usage = 69.2 }) => {
    return (
        <Paper elevation={1} sx={{
            p: 3, flex: 1, borderRadius: 3, border: '1px solid #ececec',
            display: 'flex', flexDirection: 'column'
        }}>
            <Typography sx={{
                alignSelf: 'center',
                paddingBottom: 5,
                paddingTop: 2,
                fontWeight: theme => theme.typography.fontWeightMedium
            }}>
                Dashboard do Sistema
            </Typography>

            <Stack spacing={2} direction={"row"} justifyContent="center" alignItems="center">
                <Box sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}>
                    <Typography alignSelf={'center'}>
                        Uso de CPU (%)
                    </Typography>
                    <ArcGauge value={cpu_usage} isFull={true} />
                </Box>
                <Box sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}>
                    <Typography alignSelf={'center'}>
                        Uso de RAM (%)
                    </Typography>
                    <ArcGauge value={ram_usage} isFull={true} />
                </Box>
            </Stack>
        </Paper>
    )
}

export default SystemDashboard