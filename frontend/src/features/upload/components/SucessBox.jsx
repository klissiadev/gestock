import React from 'react';
import { Dialog, DialogContent, DialogContentText, DialogTitle, Slide, Box, Typography } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
});

const SucessBox = ({ open, handleClose }) => {
    return (
        <Dialog
            open={open}
            slots={{
                transition: Transition,
            }}
            keepMounted
            onClose={handleClose}
            aria-describedby="alert-dialog-slide-description"
            sx={{
                backgroundColor: theme => theme.palette.background.default
            }}
        >

            <Box sx={{
                backgroundColor: theme => theme.palette.table.main,
                borderRadius: 1
            }}>
                <DialogTitle >
                    <Box sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 2,
                        padding: 1,
                    }}>
                        <CheckCircleIcon sx={{ color: (theme) => theme.palette.button.icon }} />
                        <Typography variant="h6" sx={{ fontWeight: theme => theme.typography.fontWeightLight, fontFamily: theme => theme.typography.fontFamily }}>
                            Planilha anexada
                        </Typography>
                    </Box>
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-slide-description">
                        Importação realizada com sucesso!
                        Os dados da planilha foram carregados e já podem ser visualizados no estoque.
                    </DialogContentText>
                </DialogContent>
            </Box>
        </Dialog>
    );
}

export default SucessBox