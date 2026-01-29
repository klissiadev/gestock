
import {IconButton, InputBase, Toolbar } from '@mui/material';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';
import ArrowCircleUpRoundedIcon from '@mui/icons-material/ArrowCircleUpRounded';

export const SearchBar = () => {
    // To Do
    const toolbar = {
        display: 'flex',
        justifyContent: 'space-between',
        gap: 2,
        borderStyle: 'solid',
        borderWidth: '2px',
        borderRadius: 4,
    }

    const searchbutton = { 
        color: (theme) => theme.palette.common.black,
    }

    return (
        <Toolbar sx={toolbar}>
            <SearchOutlinedIcon />

            <InputBase
                id="search"
                placeholder='Buscar seu produto...'
                sx={{
                    flex: 1,
                    '::placeholder': {
                        fontFamily: theme => theme.typography.fontFamily,
                        fontWeight: theme => theme.typography.fontWeightLight
                    }
                }}
            />

            <IconButton size='large' sx={searchbutton}>
                <ArrowCircleUpRoundedIcon />
            </IconButton>

        </Toolbar>
    )
}

export default SearchBar
