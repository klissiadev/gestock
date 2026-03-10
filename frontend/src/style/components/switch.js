const MuiSwitch = {
  styleOverrides: {
    root: {
      width: 34,
      height: 20,
      padding: 0,
      display: "flex",
      alignItems: "center",
      backgroundColor: ""
    },

    thumb: {
      width: 16,
      height: 16,
      boxShadow: "none",
      backgroundColor: "#fff",
    },

    track: ({ theme }) => ({
      borderRadius: 10,
      backgroundColor: theme.palette.iconButton.hover,
      opacity: 1,
    }),

    switchBase: ({ theme }) => ({
      padding: 2,

      "&.Mui-checked": {
        transform: "translateX(14px)",

        "& + .MuiSwitch-track": {
          backgroundColor: theme.palette.iconButton.active, // cor quando ligado
        },
      },
    }),
  },
};

export default MuiSwitch;