import { useEffect, useState, useCallback } from 'react';
import { Box, Divider, Stack } from '@mui/material';
import { fetchHardware } from './services/fetchHardware';
import { fetchHealth } from './services/fetchHealth';

import SystemDashboard from './components/SystemDashboard';
import GPUDashboard from './components/GPUDashboard';
import ServiceFooter from './components/ServiceFooter';

const AdminPage = () => {
    const [info, setInfo] = useState(null);
    const [healthInfo, setHealthInfo] = useState(null);
    const [loading, setLoading] = useState(true);

    const refreshDashboard = useCallback(async () => {
        try {
            const [hwData, healthData] = await Promise.all([
                fetchHardware(),
                fetchHealth()
            ]);
            setInfo(hwData);
            setHealthInfo(healthData);
            console.log(healthInfo)
        } catch (error) {
            console.error("Erro ao atualizar dashboard:", error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        refreshDashboard();
        const intervalId = setInterval(refreshDashboard, 5000);
        return () => clearInterval(intervalId);
    }, [refreshDashboard]);

    if (loading) return <Box sx={{ p: 5, textAlign: 'center' }}>Carregando...</Box>;
    if (!info) return null;

    return (
        <Box sx={{ p: 3, width: '100%', display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Stack direction="row" spacing={3} sx={{ width: '100%', alignItems: 'stretch' }}>
                {/* Seção 1: Ocupa 1 parte*/}
                <Box sx={{ flex: 1, display: 'flex' }}>
                    <SystemDashboard cpu_usage={info.cpu} ram_usage={info.ram} />
                </Box>

                {/* Seção 2: Ocupa 2 partes */}
                <Box sx={{ flex: 2, display: 'flex' }}>
                    <GPUDashboard
                        gpu_name={info.gpu.name}
                        gpu_temp={info.gpu.temp}
                        gpu_usage={info.gpu.usage}
                        gpu_vram_usage={info.gpu.vram_used_mb}
                    />
                </Box>
            </Stack>

            <Divider sx={{ my: 4 }} />

            <Box sx={{ width: '100%' }}>
                <ServiceFooter
                    ollama={healthInfo.ollama}
                    database={healthInfo.database}
                    smtp={healthInfo.google_smtp}
                    uptime={info.uptime}
                />
            </Box>
        </Box>

    );
};

export default AdminPage;