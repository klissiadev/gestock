import {
    Card, CardContent,
    Typography, TableContainer,
    Table, TableHead, TableRow,
    TableCell, TableBody, Paper,
    Chip, LinearProgress, Tooltip, Box
} from "@mui/material";
import { alpha } from "@mui/material/styles";

const DAYS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

export const ForecastTable = ({ filteredData, loading }) => (
    <Card sx={{ bgcolor: "card.background" }}>
        <CardContent sx={{ pb: "16px !important" }}>
            <Typography variant="caption" sx={{ color: "text.secondary", textTransform: "uppercase", letterSpacing: 1, display: "block", mb: 2 }}>
                Registros Detalhados
            </Typography>
            <TableContainer component={Paper} sx={{ 
                    maxHeight: "calc(100vh - 600px)",
                    overflow: "auto",
                    borderRadius: "8px",
                    border: "1px solid",
                    borderColor: "divider"
                }}>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            {["Status", "Nome", "Quantidade", "Preço (R$)", "Tipo", "Score de Erro", "Loja"].map(h => (
                                <TableCell key={h} sx={{ color: "text.secondary", fontWeight: 600, fontSize: 11, letterSpacing: 0.5, textTransform: "uppercase", fontFamily: "inherit" }}>
                                    {h}
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filteredData.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={8} align="center" sx={{ py: 4, color: "text.secondary", fontFamily: "inherit" }}>
                                    {loading ? "Carregando..." : "Nenhum registro encontrado."}
                                </TableCell>
                            </TableRow>
                        ) : filteredData.map((row, i) => (
                            <TableRow
                                key={i}
                                sx={{
                                    bgcolor: row.result === -1 ? alpha("#ff3d6e", 0.04) : "transparent",
                                    "&:hover": { bgcolor: alpha("#00e5ff", 0.04) },
                                }}>
                                <TableCell>
                                    <Chip
                                        label={row.result === -1 ? "ANOMALIA" : "NORMAL"}
                                        size="small"
                                        sx={{
                                            bgcolor: row.result === -1 ? alpha("#ff3d6e", 0.15) : alpha("#26a269", 0.15),
                                            color: row.result === -1 ? "#ff3d6e" : "#26a269",
                                            fontWeight: 700, fontSize: 10, fontFamily: "inherit", height: 20,
                                        }}
                                    />
                                </TableCell>
                                <TableCell sx={{ fontFamily: "inherit" }}>{row.nome}</TableCell>
                                <TableCell sx={{ fontFamily: "inherit" }}>{row.quantidade}</TableCell>
                                <TableCell sx={{ fontFamily: "inherit" }}>{Number(row.preco_de_venda)?.toLocaleString("pt-BR")}</TableCell>
                                <TableCell sx={{ color: "text.secondary", fontFamily: "inherit" }}>{row.tipo}</TableCell>
                                <TableCell sx={{ fontFamily: "inherit" }}>{row.cliente}</TableCell>
                                {/* Nova coluna de Score/Confiança */}
                                <TableCell>
                                    <Tooltip title={`Score: ${row.score.toFixed(4)}`}>
                                        <Box sx={{ width: '100%', minWidth: 60 }}>
                                            <Typography variant="caption" sx={{ fontSize: 10, display: 'block' }}>
                                                Intensidade
                                            </Typography>
                                            <LinearProgress
                                                variant="determinate"
                                                value={Math.min(Math.abs(row.score) * 100, 100)}
                                                color={row.result === -1 ? "error" : "success"}
                                                sx={{ height: 4, borderRadius: 2 }}
                                            />
                                        </Box>
                                    </Tooltip>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </CardContent>
    </Card>
);