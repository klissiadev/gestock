import { useState } from 'react'
import { Select, FormControl, MenuItem } from '@mui/material'

const orderSelector = {
    borderStyle: 'solid',
    borderWidth: '2px',
    borderRadius: 4,
    borderColor: (theme) => theme.palette.common.black,
    "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
        borderWidth: 0
    }
}

const menuItem = {
    '&:hover': {
        backgroundColor: (theme) => theme.palette.table.hover
    },
    '&.Mui-selected': {
        backgroundColor: (theme) => theme.palette.table.hover
    },
    '&.Mui-selected:hover': {
        backgroundColor: (theme) => theme.palette.table.hover
    },
    '&:focus': {
        backgroundColor: (theme) => theme.palette.table.hover
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
