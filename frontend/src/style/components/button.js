// button.jsx
const MuiButton = {
  defaultProps: {
    disableRipple: true,
  },

  styleOverrides: {
    root: ({ theme }) => ({
      width: 190,
      height: 40,
      backgroundColor: theme.palette.iconButton.main,
      gap:8,  
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: theme.palette.common.black,
      boxShadow: "none",
      fontSize:16,

        transition: theme.transitions.create(
            ["background-color", "transform"],
            { duration: 150 }
        ),

        "&:hover": {
            backgroundColor: theme.palette.iconButton.hover,
            boxShadow: "none",
        },

        "&.Mui-selected": {
            backgroundColor: theme.palette.iconButton.selected,

            "&:hover": {
            backgroundColor: theme.palette.iconButton.active,
            },
        },

        "&:focus": {
            outline: "none",
            boxShadow: "none",
        },

        "& .MuiSvgIcon-root": {
            fontSize: 20  ,
        },
    }),
  },
};

export default MuiButton;
