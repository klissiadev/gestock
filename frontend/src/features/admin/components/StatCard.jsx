import React from 'react';
import { Paper, Typography, Box, Stack, Chip, useTheme } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import InfoIcon from '@mui/icons-material/Info';

// Componente de Cardzinho
const StatCard = ({ 
  title, 
  value, 
  description, 
  type = 'text', // 'text' ou 'service'
  status = 'online', // 'online', 'offline', 'warning'
  icon: CustomIcon,
  customBGC
}) => {


  // Configuração de cores e ícones baseada no status do serviço
  const statusConfig = {
    online: { color: theme => theme.palette.success.main, icon: <CheckCircleIcon fontSize="small" /> },
    warning: { color: theme => theme.palette.warning.main, icon: <InfoIcon fontSize="small" /> },
    offline: { color: theme => theme.palette.error.main, icon: <ErrorIcon fontSize="small" /> },
  };

  const currentStatus = statusConfig[status] || statusConfig.online;
  const bg = theme => (customBGC || theme.palette.admin.secondary);

  return (
    <Paper 
      elevation={2} 
      sx={{ 
        p: 2, 
        width: '100%', 
        maxWidth: 280, 
        borderRadius: 3, 
        minHeight: 120,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        backgroundColor: customBGC,
        color: (theme) => {
          const bgColor = typeof customBGC === 'function' ? customBGC(theme) : customBGC;
          return bgColor ? theme.palette.getContrastText(bgColor) : 'text.primary';
        },
        transition: 'all 0.3s ease',
        '&:hover': { filter: 'brightness(0.95)' }
      }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
        {/* Titulo aqui */}
        <Typography variant="caption" fontWeight="light" sx={{ textTransform: 'uppercase' }}>
          {title}
        </Typography>
        {/* Ícone decorativo ou o izinho padrao*/}
        {CustomIcon ? <CustomIcon sx={{ fontSize: 20 }} /> : <InfoIcon sx={{ color: 'text.disabled', fontSize: 20 }} />}
      </Stack>

      <Box sx={{ my: 1 }}>
        {/* O que diferencia info de serviço pra só texto */}
        {type === 'service' ? (
          <Stack direction="row" alignItems="center" spacing={1}>
            <Box sx={{ color: currentStatus.color, display: 'flex' }}>
              {currentStatus.icon}
            </Box>
            <Typography fontFamily={theme => theme.typography.fontFamily} fontWeight={theme => theme.typography.fontWeightMedium}>
              {value}
            </Typography>
          </Stack>
        ) : (
          <Typography fontFamily={theme => theme.typography.fontFamily} fontWeight={theme => theme.typography.fontWeightMedium} sx={{ wordBreak: 'break-word' }}>
            {value}
          </Typography>
        )}
      </Box>

      <Stack direction="row" justifyContent="space-between" alignItems="center">
        {/* O textinho pequeno no fundo */}
        <Typography variant="caption">
          {description}
        </Typography>
        {type === 'service' && (
          <Chip 
            label={status} 
            size="small" 
            sx={{ 
              height: 16, 
              fontSize: '0.65rem', 
              backgroundColor: currentStatus.color + '20',
              color: currentStatus.color,
              fontFamily: theme => theme.typography.fontFamily,
              fontWeight: theme => theme.typography.fontWeightMedium,
              textTransform: 'uppercase'
            }} 
          />
        )}
      </Stack>
    </Paper>
  );
};

export default StatCard;