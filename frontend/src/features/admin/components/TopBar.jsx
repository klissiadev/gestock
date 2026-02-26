import React from "react";
import { Box, Typography, Stack, Divider } from "@mui/material";
import OrderSelector from "../../stock/components/OrderSelector";
import SearchBar from "../../stock/components/SearchBar";

const TopBar = ({
  title,
  icon: Icon,
  filters,
  onFilterChange,
  orderOptions = [],
  searchPlaceholder = "Buscar...",
  rightContent = null,
}) => {
  return (
    <Stack px={1}>
      {/* Header */}
      <Stack direction="row" alignItems="center" pb={1}>
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 2,
          }}
        >
          {Icon && <Icon width={24} height={24} />}
          <Typography fontSize={20} fontWeight={500}>
            {title}
          </Typography>
        </Box>
      </Stack>

      <Divider variant="middle" />

      {/* Filters */}
      <Stack direction="row" alignItems="center" mt={1}>
        {/* Order */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-start",
            gap: 1,
          }}
        >
          {orderOptions.length > 0 && (
            <OrderSelector
              name="order"
              value={filters.order}
              onChange={onFilterChange}
              options={orderOptions}
              placeholder="Ordenar por"
              startingPoint=""
            />
          )}
        </Box>

        {/* Search */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <SearchBar
            value={filters.searchTerm}
            onChange={onFilterChange}
            name="searchTerm"
            placeholder={searchPlaceholder}
          />
        </Box>

        {/* Right Extra */}
        <Box
          sx={{
            flex: 1,
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          {rightContent}
        </Box>
      </Stack>
    </Stack>
  );
};

export default TopBar;