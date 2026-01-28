import { createTheme } from '@mui/material/styles';

import { palette } from './pallette';
import { typography } from './typography';
import MuiIconButton from './components/iconButton';
import MuiDrawer from './components/drawer';
import MuiButton from './components/button';

export const theme = createTheme({
    // Colocar aqui os componentes
    palette,
    typography,
        
    components: {
        MuiDrawer,
        MuiIconButton,
        MuiButton,
    },
});

// Tutorial
// Usando as cores da Paleta

// color=theme.palette.table.main
// theme.palette.iconButton.main
