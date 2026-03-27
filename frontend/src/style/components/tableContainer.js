export const MuiTableContainer = {
  styleOverrides: {
    root: ({ theme }) => ({
      backgroundColor: theme.palette.table.main,
      borderRadius: 8,
      overflow: "auto",
      maxHeight: "100vh",
      boxShadow: theme.shadows[3],
      flex: 1
    }),
  },
};