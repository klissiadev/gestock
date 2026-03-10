import { Paper, Typography, Stack } from '@mui/material'
import ArcGauge from './ArcGauge'
import StatCard from './StatCard'
import SensorsIcon from '@mui/icons-material/Sensors';
import MemoryIcon from '@mui/icons-material/Memory';

const GPUDashboard = ({ gpu_name = "RTX 9090 XT", gpu_usage = 8, gpu_vram_usage = 1234.3, gpu_temp = 56 }) => {
  return (
    <Paper elevation={1} sx={{
      p: 3, flex: 1, borderRadius: 3, border: '1px solid #ececec',
      display: 'flex', flexDirection: 'column'
    }}>
      <Typography variant="h6" textAlign="center" sx={{ mb: 2, fontWeight: 'bold' }}>
        GPU Info
      </Typography>
      {/* Rodapé: GPU INFO */}
      <Stack direction="column" spacing={2} sx={{ mt: 3 }}>
        <ArcGauge value={gpu_usage} isFull={false} />
        <Typography variant="body2" sx={{ mt: 1, color: 'text.secondary', alignSelf: 'center' }}>
          Uso de GPU (%)
        </Typography>
      </Stack>

      {/* Rodapé: As 3 métricas */}
      <Stack direction="row" spacing={6} sx={{ mt: 3 }}>
        <StatCard title="VRAM Usada (MB)" value={gpu_vram_usage}
          icon={MemoryIcon}
          customBGC={(theme) => theme.palette.admin.secondary} flex={1} />
        <StatCard title="Nome da GPU" value={gpu_name}
          customBGC={(theme) => theme.palette.admin.secondary} flex={1} />
        <StatCard title="Temperatura (ºC)" value={gpu_temp ? `${gpu_temp}ºC` : 'N/A'}
          icon={SensorsIcon}
          customBGC={(theme) => theme.palette.admin.secondary} flex={1} />
      </Stack>
    </Paper>
  );
};

export default GPUDashboard