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
    <Grid container spacing={3}>
        {/* Gráfico de Barras - 100% da largura da coluna */}
        <Grid item xs={12} sx={{height: "calc(100vh - 550px)",}}>
            <Card sx={{ p: 3, borderRadius: "16px" }}>
                <Typography variant="h6" sx={{ fontSize: "16px", mb: 2, fontWeight: 600 }}>
                    Anomalias por Dia da Semana
                </Typography>
                <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={byDay}>
                        <CartesianGrid stroke="#f0f0f0" vertical={false} />
                        <XAxis dataKey="day" axisLine={false} tickLine={false} />
                        <YAxis axisLine={false} tickLine={false} />
                        <Tooltip content={<BarTooltip />} />
                        <Bar dataKey="Anomalias" fill="#ff3d6e" radius={[4, 4, 0, 0]} barSize={30} />
                        <Bar dataKey="Normais" fill="#26a269" radius={[4, 4, 0, 0]} barSize={30} />
                    </BarChart>
                </ResponsiveContainer>
            </Card>
        </Grid>

        {/* Gráfico de Pizza - Agora com espaço de sobra! */}
        <Grid item xs={12}>
            <Card sx={{ p: 3, borderRadius: "16px" }}>
                <Typography variant="h6" sx={{ fontSize: "16px", mb: 2, fontWeight: 600 }}>
                    Distribuição por Categoria
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                        <Pie 
                            data={byCat} 
                            innerRadius={70} 
                            outerRadius={100} 
                            paddingAngle={5} 
                            dataKey="value"
                        >
                            {byCat.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={PIE_COLS[index % PIE_COLS.length]} />
                            ))}
                        </Pie>
                        <Tooltip />
                        <Legend verticalAlign="bottom" height={36}/>
                    </PieChart>
                </ResponsiveContainer>
            </Card>
        </Grid>
    </Grid>
);