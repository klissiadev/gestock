import { createTheme } from '@mui/material/styles';

import { palette } from './pallette';
import { typography } from './typography';
import MuiIconButton from './components/iconButton';
import MuiDrawer from './components/drawer';
import MuiButton from './components/button';
import MuiListItemButton from './components/listItemButton';
import MuiListItemIcon from './components/listItemIcon';
import { MuiTable } from './components/table';
import { MuiTableRow } from './components/tableRow';
import { MuiTableCell } from './components/tableCell';
import { MuiTableHead } from './components/tableHead';
import { MuiTableContainer } from './components/tableContainer';

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
        MuiTable,
        MuiTableRow,
        MuiTableCell,
        MuiTableHead,
        MuiTableContainer,
    },
});

// Tutorial
// Usando as cores da Paleta

// color=theme.palette.table.main
// theme.palette.iconButton.main
