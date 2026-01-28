import { createTheme } from '@mui/material/styles';

import { palette } from './pallette';
import MuiIconButton from './components/iconButton';
import MuiDrawer from './components/drawer';
import MuiListItemButton from './components/listItemButton';

export const theme = createTheme({
    // Colocar aqui os componentes
    palette,
        
    components: {
        MuiDrawer,
        MuiIconButton,
        MuiListItemButton,
    },
});

// Tutorial
// Usando as cores da Paleta

// color=theme.palette.table.main
// theme.palette.iconButton.main
