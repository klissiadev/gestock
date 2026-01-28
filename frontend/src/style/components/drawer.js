const MuiDrawer = {
  
  styleOverrides: {
    root: ({ theme }) => ({
      "& .MuiDrawer-paper": {
        width: 60,
        padding: "6px 6px",
         // 🔥 ISSO RESOLVE
        height: "calc(100vh - 32px)",
        margin: 16,
        borderRadius: 12,
        display: "flex",
        flex: 1,
        flexDirection: "column",
        justifyContent: "space-between"
      },
    }),
  },
};

export default MuiDrawer;
