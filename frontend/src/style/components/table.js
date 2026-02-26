export const MuiTable = {
  defaultProps: {      
    stickyHeader: true,
  },
  styleOverrides: {
    root: ({ theme }) => ({
      backgroundColor: theme.palette.table.main,
    }),
  },
};