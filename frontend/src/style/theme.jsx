import { createTheme } from '@mui/material/styles';

import { palette } from './pallette';
import { typography } from './typography';
import MuiIconButton from './components/iconButton';
import MuiDrawer from './components/drawer';
import MuiButton from './components/button';
import MuiListItemButton from './components/listItemButton';
import MuiListItemIcon from './components/listItemIcon';
import MuiInput from './components/input';

export const theme = createTheme({
    // Colocar aqui os componentes
    palette,
    typography,
        
    components: {
        MuiDrawer,
        MuiIconButton,
        MuiButton,
        MuiListItemButton,
        MuiListItemIcon,
        MuiInput,
        MuiInputBase: {
            styleOverrides: {
                input: {
                "&:focus-visible": {
                    borderColor: "primary.main",
                    
                },
                "&:focus": {
                    borderColor: "primary.main",
                },
                },
            },
        },
    },
});

// Tutorial
// Usando as cores da Paleta

// color=theme.palette.table.main
// theme.palette.iconButton.main
