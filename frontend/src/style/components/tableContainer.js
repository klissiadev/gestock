export const MuiTableContainer = {
  styleOverrides: {
    root: ({ theme }) => ({
      backgroundColor: theme.palette.table.main,
      borderRadius: 8,
      overflow: "auto",
      maxHeight: "100%", 
      boxShadow: "0px 2px 4px rgba(0,0,0,0.05)",
    }),
  },
};