// forecast/components/ForecastKPIs.jsx
import { Grid, Card, CardContent, Typography } from "@mui/material";

export const ForecastKPIs = ({ kpis }) => (
    <>
        {kpis.map((k) => (
            <Grid item xs={12} sm={6} md={2.5} key={k.label}> {/* Largura fixa menor para centralizar melhor */}
                <Card sx={{
                    borderRadius: "16px",
                    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
                    bgcolor: "#673ab7" 
                }}>
                    <CardContent sx={{ textAlign: "center", p: "20px !important" }}>
                        <Typography variant="caption" sx={{ color: "rgba(255,255,255,0.7)", fontWeight: 600, textTransform: "uppercase" }}>
                            {k.label}
                        </Typography>
                        <Typography variant="h4" fontWeight={800} sx={{ color: "#fff", mt: 1 }}>
                            {k.value}
                        </Typography>
                    </CardContent>
                </Card>
            </Grid>
        ))}
    </>
);