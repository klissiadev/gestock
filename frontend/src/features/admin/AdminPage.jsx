import React, { useEffect, useState, useCallback } from 'react';
import { 
    Box, CircularProgress, Typography, Paper, 
    Divider, Chip, Stack 
} from '@mui/material'; // Adicionado Stack aqui
import { fetchHardware } from './services/fetchHardware';
import { fetchHealth } from './services/fetchHealth';
import UsageBox from './components/UsageBox';
import { HARDWARE_FIELDS } from './constants/hardwareConstants';
import SignalCellularAltIcon from '@mui/icons-material/SignalCellularAlt';


import SystemDashboard from './components/SystemDashboard';

const getLatencyColor = (ms) => {
    if (ms < 200) return 'success.main';
    if (ms < 800) return 'warning.main';
    return 'error.main';
};

const AdminPage = () => {
    const [info, setInfo] = useState(null);
    const [healthInfo, setHealthInfo] = useState(null);
    const [loading, setLoading] = useState(true);

    // Unificamos a busca para garantir que o dashboard atualize em sincronia
    const refreshDashboard = useCallback(async () => {
        try {
            // Promise.all executa ambas as chamadas simultaneamente (mais rápido)
            const [hwData, healthData] = await Promise.all([
                fetchHardware(),
                fetchHealth()
            ]);
            
            setInfo(hwData);
            setHealthInfo(healthData);
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
        <Box sx={{ p: 3 }}>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
                Dashboard do Sistema
            </Typography>
            
            {/* --- SEÇÃO 1: MÉTRICAS PRINCIPAIS --- */}
            <Box sx={{ display: 'flex', gap: 2, mb: 4, flexWrap: 'wrap' }}>
                <SystemDashboard cpu_usage={info.cpu} ram_usage={info.ram}/>
            </Box>

            {/* --- SEÇÃO 2: GPU --- */}
            {info.gpu && (
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h6" sx={{ mb: 2 }}>GPU Info</Typography>
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
                        {Object.entries(info.gpu).map(([subKey, subValue]) => {
                            if (subKey === 'usage') {
                                return (
                                    <UsageBox 
                                        key={subKey} 
                                        name={HARDWARE_FIELDS.gpu[subKey]} 
                                        usage={subValue} 
                                    />
                                );
                            }
                            return (
                                <Paper key={subKey} elevation={0} sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 2, minWidth: '130px' }}>
                                    <Typography variant="caption" color="textSecondary" display="block">
                                        {HARDWARE_FIELDS.gpu[subKey] || subKey.toUpperCase()}
                                    </Typography>
                                    <Typography variant="body1" fontWeight="bold">
                                        {subValue}
                                    </Typography>
                                </Paper>
                            );
                        })}
                    </Box>
                </Box>
            )}

            <Divider sx={{ my: 4 }} />

            {/* --- SEÇÃO 3: STATUS DOS SERVIÇOS --- */}
            {healthInfo && (
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h6" sx={{ mb: 2 }}>Status dos Serviços</Typography>
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                        {Object.entries(healthInfo).map(([serviceName, details]) => (
                            <Paper 
                                key={serviceName} 
                                elevation={0} 
                                sx={{ 
                                    p: 2, 
                                    border: '1px solid #e0e0e0', 
                                    borderRadius: 2,
                                    minWidth: '220px',
                                    flex: '1 1 calc(33.333% - 16px)'
                                }}
                            >
                                <Stack direction="row" justifyContent="space-between" alignItems="center">
                                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold', textTransform: 'capitalize' }}>
                                        {serviceName.replace('_', ' ')}
                                    </Typography>
                                    <Chip 
                                        label={details.status} 
                                        size="small" 
                                        color={details.status === 'Online' ? 'success' : 'error'}
                                    />
                                </Stack>

                                <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <SignalCellularAltIcon sx={{ fontSize: 16, color: getLatencyColor(details.latency) }} />
                                    <Typography variant="body2" color="textSecondary">
                                        Latência: 
                                        <Box component="span" sx={{ fontWeight: 'bold', ml: 0.5, color: getLatencyColor(details.latency) }}>
                                            {details.latency?.toFixed(2)} ms
                                        </Box>
                                    </Typography>
                                </Box>
                            </Paper>
                        ))}
                    </Box>
                </Box>
            )}

            {/* --- RODAPÉ: INFORMAÇÕES DO SISTEMA --- */}
            <Paper elevation={0} sx={{ p: 2, bgcolor: '#e3f2fd', borderRadius: 2, display: 'inline-block' }}>
                <Typography variant="body2" color="primary.main" fontWeight="500">
                    <strong>Uptime:</strong> {info.uptime}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                    Sincronizado em: {new Date().toLocaleTimeString()}
                </Typography>
            </Paper>
        </Box>
    );
};

export default AdminPage;