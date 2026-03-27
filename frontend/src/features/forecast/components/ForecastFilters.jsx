import { ToggleButtonGroup, ToggleButton } from "@mui/material";

export const ForecastFilters = ({ categories, activeCategory, setActiveCategory }) => (
    <ToggleButtonGroup
        value={activeCategory}
        exclusive
        onChange={(_, v) => v && setActiveCategory(v)}
        sx={{ flexWrap: "wrap", gap: 1, mb: 3, "& .MuiToggleButtonGroup-grouped": { mr: 0 } }}
    >
        {categories.map(cat => (
            <ToggleButton 
            key={cat}
            value={cat}
            sx={{
                textTransform: "none",
                borderRadius: 3,
                px: 1,
                p:1,
                fontSize:"12px",

                // estado ativo
                "&.Mui-selected": {
                    backgroundColor: (theme) => theme.palette.primary.main,
                    color: (theme) => theme.palette.primary.contrastText,
                    boxShadow: (theme) => theme.shadows[1],
                },

                "&.Mui-selected:hover": {
                    backgroundColor: (theme) => theme.palette.primary.dark,
                },
            }}
            >{cat}</ToggleButton>
        ))}
    </ToggleButtonGroup>
);