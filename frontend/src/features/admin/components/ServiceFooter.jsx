import StatCard from './StatCard'
import SensorsIcon from '@mui/icons-material/Sensors';
import { Paper, Stack } from '@mui/material'

const ServiceFooter = ({ database, ollama, smtp, uptime }) => {
    return (
        <Paper elevation={0} sx={{
            p: 2,
            width: '100%',
            borderRadius: 3,
            border: '1px solid #ececec',
            display: 'flex',
            flexDirection: 'column',
        }}>

            <Stack
                direction="row"
                spacing={1}
                sx={{
                    width: '100%',
                    justifyContent: 'space-between',
                    alignItems: 'stretch'
                }}
            >
                <StatCard
                    type="service"
                    title="Database"
                    value={database.status}
                    status={database.status.toLowerCase()}
                    description={"Latência: "+ database.latency}
                    icon={SensorsIcon}
                    sx={{ flex: 2 }}
                />

                <StatCard
                    type="service"
                    title="Ollama (IA Local)"
                    value={ollama.status}
                    status={ollama.status.toLowerCase()}
                    description={"Latência: "+ ollama.latency}
                    icon={SensorsIcon}
                    sx={{ flex: 2 }}
                />

                <StatCard
                    type="service"
                    title="Serviço de E-Mail Google"
                    value={smtp.status}
                    status={smtp.status.toLowerCase()}
                    description={"Latência: "+ smtp.latency}
                    icon={SensorsIcon}
                    sx={{ flex: 2 }}
                />

                <StatCard
                    title="Uptime"
                    value={uptime}
                    description={"Sincronizando em: " + new Date().toLocaleTimeString()}
                    icon={SensorsIcon}
                    customBGC={theme => theme.palette.admin.main}
                    sx={{ flex: 1 }}
                />
            </Stack>
        </Paper>
    )
}

export default ServiceFooter

