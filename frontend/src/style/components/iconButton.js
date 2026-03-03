// src\style\components\iconButton.js
const MuiIconButton = {
  defaultProps: {
    disableRipple: true,
  },

  styleOverrides: {
    root: ({ theme }) => ({
      width: 40,
      height: 40,
      padding: 0, // IMPORTANTE
      borderRadius: 4, // agora aparece
      color: theme.palette.iconButton.main,

      display: "flex",
      alignItems: "center",
      justifyContent: "center",

      transition: theme.transitions.create(
        ["background-color", "transform"],
        { duration: 150 }
      ),

      "&:hover": {
        backgroundColor: theme.palette.iconButton.hover,
      },

      "&.Mui-selected": {
        backgroundColor: theme.palette.iconButton.selected,

        "&:hover": {
          backgroundColor: theme.palette.iconButton.active,
        },
      },

      "& .MuiSvgIcon-root": {
        fontSize: 20  ,
      },
    }),
  },
};

export default MuiIconButton;
