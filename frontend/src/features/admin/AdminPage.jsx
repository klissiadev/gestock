import React, { useEffect, useState, useCallback } from 'react';
import { Box, CircularProgress, Typography, Paper, Divider } from '@mui/material';
import { fetchHardware } from './services/fetchHardware';
import UsageBox from './components/UsageBox';
import { HARDWARE_FIELDS } from './constants/hardwareConstants';

const AdminPage = () => {
    const [info, setInfo] = useState(null);
    const [loading, setLoading] = useState(true);

    const loadData = useCallback(async () => {
        try {
            const data = await fetchHardware();
            setInfo(data);
        } catch (error) {
            console.error("Erro ao buscar hardware:", error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadData();
        const intervalId = setInterval(loadData, 5000);
        return () => clearInterval(intervalId);
    }, [loadData]);

    if (loading) return <Box sx={{ p: 5, textAlign: 'center' }}><CircularProgress /></Box>;
    if (!info) return null;

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>Dashboard de Hardware</Typography>
            
            {/* --- SEÇÃO 1: MÉTRICAS PRINCIPAIS (CPU e RAM) --- */}
            <Box sx={{ display: 'flex', gap: 2, mb: 4, flexWrap: 'wrap' }}>
                <UsageBox name={HARDWARE_FIELDS.cpu} usage={info.cpu} />
                <UsageBox name={HARDWARE_FIELDS.ram} usage={info.ram} />
            </Box>

            <Divider sx={{ mb: 4 }} />

            {/* --- SEÇÃO 2: DESTRINCHANDO A GPU --- */}
            {info.gpu && (
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h6" sx={{ mb: 2 }}>GPU Info</Typography>
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
                        {Object.entries(info.gpu).map(([subKey, subValue]) => {
                            // IMPORTANTE: Aqui usamos { } e precisamos do return explícito
                            if (subKey === 'usage') {
                                return (
                                    <UsageBox 
                                        key={subKey} 
                                        name={HARDWARE_FIELDS.gpu[subKey]} 
                                        usage={subValue} 
                                    />
                                );
                            } else {
                                return (
                                    <Paper key={subKey} elevation={0} sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 2, minWidth: '120px' }}>
                                        <Typography variant="caption" color="textSecondary" display="block">
                                            {HARDWARE_FIELDS.gpu[subKey]}
                                        </Typography>
                                        <Typography variant="body1" fontWeight="bold">
                                            {subValue.toFixed(2)}
                                        </Typography>
                                    </Paper>
                                );
                            }
                        })}
                    </Box>
                </Box>
            )}

            {/* --- SEÇÃO 3: INFORMAÇÕES DE SISTEMA (UPTIME) --- */}
            <Paper elevation={0} sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 2, display: 'inline-block' }}>
                <Typography variant="body2" color="textSecondary">
                    <strong>Tempo de Atividade:</strong> {info.uptime}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                    Última atualização: {new Date().toLocaleTimeString()}
                </Typography>
            </Paper>
        </Box>
    );
};

export default AdminPage;