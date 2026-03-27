import { Grid, Card, Typography, Stack, Paper } from "@mui/material";
import { alpha } from "@mui/material/styles";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";

const PIE_COLS = ["#ff3d6e", "#ff7043", "#ffd600", "#ab47bc", "#42a5f5"];

const BarTooltip = ({ active, payload, label }) => {
    if (!active || !payload?.length) return null;
    return (
        <Paper sx={{ p: 1.5, fontSize: 12, border: "1px solid", borderColor: "divider" }}>
            <Typography variant="caption" fontWeight={700} display="block" mb={0.5}>{label}</Typography>
            {payload.map(p => (
                <Typography key={p.name} variant="caption" display="block" sx={{ color: p.fill }}>
                    {p.name}: <b>{p.value}</b>
                </Typography>
            ))}
        </Paper>
    );
};

export const ForecastCharts = ({ byDay, byCat }) => (
    <Grid container spacing={2} mb={3}>
        {/* Bar Chart */}
        <Grid item xs={12} md={8}>
            <Card sx={{ p: 2.5, borderRadius:"14px"}}>
                <Typography variant="caption" sx={{ color: "text.secondary",fontSize:"14px", letterSpacing: 1, display: "block", mb: 2 }}>
                    Anomalias por Dia da Semana
                </Typography>
                <ResponsiveContainer width="100%" height={230}>
                    <BarChart data={byDay} barCategoryGap="30%" margin={{ top: 5, right: 10, bottom: 0, left: -10 }}>
                        <CartesianGrid stroke="#1e2535" strokeDasharray="3 3" />
                        <XAxis dataKey="day" tick={{ fill: "#7a8299", fontSize: 12, fontFamily: "inherit" }} />
                        <YAxis tick={{ fill: "#7a8299", fontSize: 11, fontFamily: "inherit" }} />
                        <Tooltip content={<BarTooltip />} cursor={{ fill: alpha("#00e5ff", 0.05) }} />
                        <Bar dataKey="Anomalias" fill="#ff3d6e" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Normais" fill="#26a269" radius={[4, 4, 0, 0]} />
                    </BarChart>
                </ResponsiveContainer>
            </Card>
        </Grid>

        {/* Pie Chart */}
        <Grid item xs={12} md={4}>
            <Card sx={{ p: 2.5, height: "100%", borderRadius:"14px"}}>
                <Typography variant="caption" sx={{ color: "text.secondary", fontSize:"14px", letterSpacing: 1, display: "block", mb: 2 }}>
                    Anomalias por Categoria
                </Typography>
                {byCat.length === 0 ? (
                    <Stack height={230} justifyContent="center" alignItems="center">
                        <Typography variant="caption" color="text.secondary">Sem anomalias no período</Typography>
                    </Stack>
                ) : (
                    <ResponsiveContainer width="100%" height={230}>
                        <PieChart>
                            <Pie data={byCat} cx="50%" cy="45%" innerRadius={52} outerRadius={80} dataKey="value" nameKey="name" paddingAngle={3}>
                                {byCat.map((_, i) => <Cell key={i} fill={PIE_COLS[i % PIE_COLS.length]} />)}
                            </Pie>
                            <Tooltip
                                contentStyle={{ background: "#111520", border: "1px solid #1e2535", borderRadius: 8, fontFamily: "inherit", fontSize: 12, color: "#e2e8f0" }}
                            />
                            <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 11, color: "#7a8299", fontFamily: "inherit" }} />
                        </PieChart>
                    </ResponsiveContainer>
                )}
            </Card>
        </Grid>
    </Grid>
);