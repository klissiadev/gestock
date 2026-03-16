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
import MuiInput from './components/input';
import { MuiPaper } from './components/errorBox';
import MuiTextField from "./components/textField";
import MuiSwitch from "./components/switch"


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
        MuiInput,
        MuiPaper,
        MuiTextField,
        MuiSwitch,
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
        MuiCssBaseline: {
            styleOverrides: {
            body: {
                /* Firefox */
                scrollbarWidth: "none",
            },

            /* Chrome, Edge, Safari */
            "::-webkit-scrollbar": {
                width: "8px",
                height: "8px",
            },

            "::-webkit-scrollbar-track": {
                background: "transparent",
            },

            "::-webkit-scrollbar-thumb": {
                backgroundColor: "transparent",
                borderRadius: "8px",
                transition: "background-color 0.3s ease",
            },

            /* quando passa o mouse em QUALQUER área scrollável */
            "*:hover::-webkit-scrollbar-thumb": {
                backgroundColor: "rgba(0,0,0,0.35)",
            },

            /* Firefox hover */
            "*:hover": {
                scrollbarWidth: "thin",
            },
            },
        },
    },
});

// Tutorial
// Usando as cores da Paleta

// color=theme.palette.table.main
// theme.palette.iconButton.main
