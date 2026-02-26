const MuiDrawer = {
  
  styleOverrides: {
    root: ({ theme }) => ({
      "& .MuiDrawer-paper": {
        padding: "6px 6px",
        height: "calc(100vh - 32px)",
        margin: 16,
        borderRadius: 12,
        display: "flex",
        flex: 1,
        flexDirection: "column",
        justifyContent: "space-between",
        backgroundColor: theme.palette.iconButton.main
      },
    }),
  },
};

export default MuiDrawer;
