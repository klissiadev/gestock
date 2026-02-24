import React, { useEffect, useState, useCallback } from 'react';
import { 
    Box, CircularProgress, Typography, Paper, 
    Divider, Chip, Stack, Grid, IconButton, Tooltip 
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import SignalCellularAltIcon from '@mui/icons-material/SignalCellularAlt';
import StorageIcon from '@mui/icons-material/Storage';

import { fetchHealth, fetchHardware } from './services/fetchHealth';
import UsageBox from './components/UsageBox';
import { HARDWARE_FIELDS } from './constants/hardwareConstants';

// --- UTILITÁRIOS ---
const getLatencyColor = (ms) => {
    if (ms < 200) return 'success';
    if (ms < 800) return 'warning';
    return 'error';
};

const AdminPage = () => {
    const [info, setInfo] = useState(null);
    const [healthInfo, setHealthInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [lastSync, setLastSync] = useState(new Date());

    const refreshDashboard = useCallback(async () => {
        try {
            const [hwData, healthData] = await Promise.all([
                fetchHardware(),
                fetchHealth()
            ]);
            setInfo(hwData);
            setHealthInfo(healthData);
            console.log("Dashboard atualizado com sucesso:", hwData, healthData);
            setLastSync(new Date());
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

    if (loading) return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <CircularProgress />
        </Box>
    );

    return (
        <Box sx={{ p: 3, maxWidth: 1800, margin: '0 auto' }}>
            
            {/* CABEÇALHO DINÂMICO */}
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 4 }}>
                <Box>
                    <Typography variant="h4" fontWeight="800" color="primary">
                        Status do Sistema
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                        Monitoramento em tempo real da infraestrutura Gestock
                    </Typography>
                </Box>
                <Tooltip title="Atualizar agora">
                    <IconButton onClick={refreshDashboard} color="primary">
                        <RefreshIcon />
                    </IconButton>
                </Tooltip>
            </Stack>

            {/* SEÇÃO 1: HARDWARE (CPU, RAM, GPU) */}
            <Typography variant="overline" color="textSecondary" sx={{ fontWeight: 'bold' }}>Hardware Principal</Typography>
            <Grid container spacing={3} sx={{ mt: 0.5, mb: 5 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <UsageBox name={HARDWARE_FIELDS.cpu} usage={info.cpu} />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <UsageBox name={HARDWARE_FIELDS.ram} usage={info.ram} />
                </Grid>
                {info.gpu && (
                    <Grid item xs={12} sm={6} md={3}>
                        <UsageBox 
                            name={HARDWARE_FIELDS.gpu.usage} 
                            usage={info.gpu.usage} 
                        />
                    </Grid>
                )}
                <Grid item xs={12} sm={6} md={3}>
                    <Paper elevation={0} sx={{ p: 2, bgcolor: 'primary.light', color: 'white', borderRadius: 3, height: '100%' }}>
                        <Typography variant="caption" sx={{ opacity: 0.8 }}>Tempo de Atividade</Typography>
                        <Typography variant="h6" fontWeight="bold">{info.uptime}</Typography>

                        <Divider sx={{ my: 2, borderColor: 'rgba(255,255,255,0.3)' }} />

                        <Stack direction="column" alignItems="center" spacing={1}>
                            <Typography variant="body2" sx={{ ml: 'auto', fontWeight: '700' }}>
                                {info.gpu ? `GPU: ${info.gpu.name}` : 'Sem GPU Detectada'}
                            </Typography>
                            <Typography variant="body2" sx={{ ml: 'auto', fontWeight: '700' }}>
                                {info.gpu ? `VRAM em uso: ${info.gpu.vram_used_mb}` : 'VRAM indisponível'}
                            </Typography>
                            <Typography variant="body2" sx={{ ml: 'auto', fontWeight: '700' }}>
                                {info.gpu ? `VRAM total: ${info.gpu.vram_total_mb}` : 'VRAM indisponível'}
                            </Typography>
                            <Typography variant="body2" sx={{ ml: 'auto', fontWeight: '700' }}>
                                {info.gpu ? `Temperatura: ${info.gpu.temp} ºC` : 'Temperatura indisponível'}
                            </Typography>
                        </Stack>
                    </Paper>
                </Grid>
            </Grid>

            {/* SEÇÃO 2: GRID DE SERVIÇOS */}
            <Typography variant="overline" color="textSecondary" sx={{ fontWeight: 'bold' }}>Microserviços & API</Typography>
            <Grid container spacing={2} sx={{ mt: 0.5, mb: 4 }}>
                {healthInfo && Object.entries(healthInfo).map(([service, details]) => (
                    <Grid item xs={12} sm={6} md={4} key={service}>
                        <Paper 
                            variant="outlined" 
                            sx={{ 
                                p: 2, 
                                borderRadius: 3, 
                                transition: '0.3s',
                                '&:hover': { boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }
                            }}
                        >
                            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
                                <Typography variant="subtitle1" fontWeight="700" sx={{ textTransform: 'capitalize' }}>
                                    {service.replace('_', ' ')}
                                </Typography>
                                <Chip 
                                    label={details.status} 
                                    size="small" 
                                    color={details.status === 'Online' ? 'success' : 'error'}
                                    sx={{ fontWeight: 'bold', borderRadius: '6px' }}
                                />
                            </Stack>
                            
                            <Stack direction="row" spacing={1} alignItems="center">
                                <SignalCellularAltIcon 
                                    color={getLatencyColor(details.latency)} 
                                    sx={{ fontSize: 18 }} 
                                />
                                <Typography variant="body2" color="textSecondary">
                                    Latência: 
                                    <Box component="span" sx={{ ml: 1, fontWeight: '700', color: `${getLatencyColor(details.latency)}.main` }}>
                                        {details.latency?.toFixed(2)} ms
                                    </Box>
                                </Typography>
                            </Stack>
                        </Paper>
                    </Grid>
                ))}
            </Grid>

            <Divider sx={{ mb: 3 }} />

            {/* RODAPÉ TÉCNICO */}
            <Stack direction="row" justifyContent="flex-end" spacing={2}>
                <Typography variant="caption" color="textDisabled">
                    Sincronizado às: {lastSync.toLocaleTimeString()}
                </Typography>
                <Typography variant="caption" color="textDisabled">
                    Versão do Sistema: v1.0.4-beta
                </Typography>
            </Stack>
        </Box>
    );
};

export default AdminPage;