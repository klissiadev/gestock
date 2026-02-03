import React from 'react'
import { FormControl, Select, MenuItem } from '@mui/material'
import { typeSelector, menuItem } from '../styles/style'

const TypeSelector = ({ value, onChange, name, options}) => {
    return (
        <FormControl fullWidth sx={{ borderColor: theme => theme.palette.common.black }}>
            <Select
                value={value}
                size='small'
                displayEmpty
                onChange={(e) => onChange(e.target.value)}
                sx={typeSelector}
            >
                {options.map((opt) => (
                    <MenuItem sx={menuItem} key={opt.value} value={opt.value}>
                        {opt.label}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>

    )
}

export default TypeSelector
