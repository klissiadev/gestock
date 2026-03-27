import { Grid, Card, CardContent, Typography } from "@mui/material";

export const ForecastKPIs = ({ kpis }) => (
    <Grid container spacing={2} mb={3}>
        {kpis.map(k => (
            <Grid item xs={12} sm={6} md={3} key={k.label}>
                <Card>
                    <CardContent sx={{ pb: "16px !important" }}>
                        <Typography variant="caption" sx={{ color: "text.secondary", textTransform: "uppercase", letterSpacing: 1 }}>
                            {k.label}
                        </Typography>
                        <Typography variant="h4" fontWeight={800} letterSpacing={-1} sx={{ color: k.color, mt: 0.5 }}>
                            {k.value}
                        </Typography>
                    </CardContent>
                </Card>
            </Grid>
        ))}
    </Grid>
);