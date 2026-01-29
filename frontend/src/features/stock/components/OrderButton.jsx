import { useState } from 'react';
import { FormControl, IconButton } from '@mui/material';
import ArrowUpwardRoundedIcon from '@mui/icons-material/ArrowUpwardRounded';
import ArrowDownwardRoundedIcon from '@mui/icons-material/ArrowDownwardRounded';
import { theme } from '../../../style/theme';

const OrderButton = () => {
    const [isAsc, setAsc] = useState(true)



    return (
        <FormControl fullWidth>
            <IconButton size='large'
                sx={{
                    padding: 3, color: (theme) => theme.palette.common.black, borderStyle: 'solid',
                    borderWidth: '1px',
                }}
                onClick={() => setAsc(!isAsc)}>
                {
                    isAsc === true ? (
                        <ArrowUpwardRoundedIcon fontSize='inherit' />
                    ) : (
                        <ArrowDownwardRoundedIcon fontSize='inherit' />
                    )
                }
            </IconButton>
        </FormControl>
    )
}

export default OrderButton
