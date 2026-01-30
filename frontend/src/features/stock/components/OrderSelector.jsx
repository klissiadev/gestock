import { useState } from 'react';
import { Select, FormControl, MenuItem } from '@mui/material';
import { theme } from '../../../style/theme';

const orderSelector = {
    backgroundColor: theme => theme.palette.button.main,
    borderStyle: 'solid',
    borderWidth: '2px',
    borderRadius: 4,
    borderColor: (theme) => theme.palette.button.main,
    "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
        borderWidth: 0
    }
}

const menuItem = {
    fontFamily: theme => theme.typography.fontFamily,
    '&:hover': {
        backgroundColor: (theme) => theme.palette.button.main
    },
    '&.Mui-selected': {
        backgroundColor: (theme) => theme.palette.button.main
    },
    '&.Mui-selected:hover': {
        backgroundColor: (theme) => theme.palette.button.main
    },
    '&:focus': {
        backgroundColor: (theme) => theme.palette.button.main
    }
}

const OrderSelector = () => {
    const [categoria, setCategoria] = useState("")

    return (
        <FormControl fullWidth>
            <Select
                value={categoria}
                displayEmpty
                onChange={(e) => setCategoria(e.target.value)}
                sx={orderSelector}
            >
                <MenuItem sx={menuItem} value="">Selecione uma categoria</MenuItem>
                <MenuItem sx={menuItem} value="A">A</MenuItem>
                <MenuItem sx={menuItem} value="B">B</MenuItem>
                <MenuItem sx={menuItem} value="C">C</MenuItem>
            </Select>
        </FormControl>
    )
}

export default OrderSelector
