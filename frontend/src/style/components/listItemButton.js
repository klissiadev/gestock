const MuiListItemButton = {
  styleOverrides: {
    root: ({ theme }) => ({
      justifyContent: "center",
      padding: 0,
      borderRadius: 16,

      "&.Mui-selected": {
        backgroundColor: "#E5E7EB",
      }
    }),
  },
};

export default MuiListItemButton;
