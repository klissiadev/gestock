import React from "react";
import {
  Box,
  Typography,
  Stack,
  Divider,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";
import ForecastSvg from "../../../assets/icon/icon-charts-purple.svg?react";

export const ForecastHeader = ({
  dateFilter,
  setDateFilter,
  onFetch,
  loading,
}) => {
  return (
    <Stack>
      {/* HEADER SUPERIOR */}
      <Stack direction="row" alignItems="center" pb={1}>

        {/* Título central */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 2,
            mb:1
          }}
        >
          <ForecastSvg width={26} height={26} />
          <Typography
            fontSize={20}
            fontWeight={500}
            sx={{ color: (theme) => theme.palette.primary.main}}
          >
            Anomaly Dashboard
          </Typography>
        </Box>
      </Stack>

      <Divider variant="middle" />

      {/* TOOLBAR / FILTROS */}
      <Stack direction="row" alignItems="center" mt={1}>
        {/* Esquerda (pode crescer depois se quiser mais filtros) */}
        <Box sx={{ flex: 1 }} />

        {/* Centro */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
            gap: 1,
          }}
        >
          <TextField
            type="date"
            size="small"
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
            sx={{
              "& .MuiOutlinedInput-root": {
                fontFamily: "inherit",
                fontSize: 13,
              },
            }}
          />

          <Button
            variant="contained"
            onClick={onFetch}
            disabled={loading}
            sx={{
              fontFamily: "inherit",
              fontWeight: 500,
              borderRadius: 2,
              textTransform: "none",
              backgroundColor: (theme) => theme.palette.primary.main,
              color: (theme) => theme.palette.common.white
            }}
          >
            {loading ? (
              <CircularProgress size={18} thickness={5} sx={{ color: "white" }} />
            ) : (
              "Buscar"
            )}
          </Button>
        </Box>

        {/* Direita */}
        <Box sx={{ flex: 1 }} />
      </Stack>
    </Stack>
  );
};