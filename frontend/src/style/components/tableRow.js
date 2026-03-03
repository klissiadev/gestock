export const MuiTableRow = {
      styleOverrides: {
        root: ({ theme }) => ({
          "&:hover": {
            backgroundColor: theme.palette.table.hover,
          },
          "&:active": {
            backgroundColor: theme.palette.background.default,
          },
        }
    )}
}