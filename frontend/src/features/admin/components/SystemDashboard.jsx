import { Box, Paper, Typography, Stack } from '@mui/material'
import ArcGauge from './ArcGauge'
import StatCard from './StatCard'

import SensorsIcon from '@mui/icons-material/Sensors';
import MemoryIcon from '@mui/icons-material/Memory';

const SystemDashboard = ({ cpu_usage = 25.5, ram_usage = 69.2 }) => {
    return (
        <Paper elevation={3} sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            flex: 1,
            fontFamily: theme => theme.typography.fontFamily,
        }}>
            <Typography sx={{
                alignSelf: 'center',
                paddingBottom: 5,
                paddingTop: 2,
                fontWeight: theme => theme.typography.fontWeightMedium
            }}>
                Dashboard do Sistema
            </Typography>

            <Stack spacing={3} direction={"row"} justifyContent="center" alignItems="center">
                <Box sx={{
                    width: { xs: '100%', sm: '200px', md: '250px' },
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
                    width: { xs: '100%', sm: '200px', md: '250px' },
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}>
                    <Typography alignSelf={'center'}>
                        Uso de RAM (%)
                    </Typography>
                    <ArcGauge value={ram_usage} isFull={true} />
                </Box>
                <Box sx={{
                    width: { xs: '100%', sm: '200px', md: '250px' },
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}>
                    <Typography alignSelf={'center'}>
                        Uso de GPU (%)
                    </Typography>
                    <ArcGauge value={12} isFull={false} />
                </Box>
            </Stack>

            {/*
            APENAS TESTES AQUI HEIN

            <StatCard
                title="Nome da GPU"
                value="NVIDIA RTX 9090"
                icon={MemoryIcon}
                customBGC={theme => theme.palette.admin.secondary}
            />

            <StatCard
                type="service"
                title="IA Local (Ollama)"
                value="Online"
                status="online"
                description="Latência: 32ms"
                icon={SensorsIcon}
                customBGC={theme => theme.palette.admin.secondary}
            />

            <StatCard
                title="Uptime"
                value="0H 32M 7s"
                description="Sincronizando em: 07:13:02"
                icon={SensorsIcon}
                customBGC={theme => theme.palette.admin.main}
            />
            
            */}

            


        </Paper>
    )
}

export default SystemDashboard