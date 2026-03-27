import { ToggleButtonGroup, ToggleButton } from "@mui/material";

export const ForecastFilters = ({ categories, activeCategory, setActiveCategory }) => (
    <ToggleButtonGroup
        value={activeCategory}
        exclusive
        onChange={(_, v) => v && setActiveCategory(v)}
        sx={{ flexWrap: "wrap", gap: 1, mb: 3, "& .MuiToggleButtonGroup-grouped": { mr: 0 } }}
    >
        {categories.map(cat => (
            <ToggleButton key={cat} value={cat}>{cat}</ToggleButton>
        ))}
    </ToggleButtonGroup>
);