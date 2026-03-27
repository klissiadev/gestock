import { Box, Typography, Stack, TextField, Button, CircularProgress } from "@mui/material";

export const ForecastHeader = ({ dateFilter, setDateFilter, onFetch, loading }) => (
    <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3.5}>
        <Box>
            <Typography variant="caption" sx={{ color: "primary.main", letterSpacing: 3, textTransform: "uppercase" }}>
                Sistema de Detecção
            </Typography>
            <Typography variant="h5" fontWeight={800} letterSpacing={-0.5} mt={0.5}>
                Anomaly Dashboard
            </Typography>
        </Box>

        <Stack direction="row" spacing={1.5} alignItems="center">
            <TextField
                type="date"
                size="small"
                value={dateFilter}
                onChange={e => setDateFilter(e.target.value)}
                sx={{ "& .MuiOutlinedInput-root": { fontFamily: "inherit", fontSize: 13 } }}
            />
            <Button
                variant="contained"
                onClick={onFetch}
                disabled={loading}
                sx={{
                    fontFamily: "inherit", fontWeight: 700, minWidth: 90,
                    bgcolor: "primary.main", color: "background.default",
                    "&:hover": { bgcolor: "#26d4ec" },
                }}
            >
                {loading ? <CircularProgress size={18} thickness={5} sx={{ color: "background.default" }} /> : "Buscar"}
            </Button>
        </Stack>
    </Stack>
);