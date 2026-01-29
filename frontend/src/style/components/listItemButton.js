// src/style/components/listItemButton.js
const MuiListItemButton = {
  defaultProps: {
    disableRipple: true,
  },

  styleOverrides: {
    root: ({ theme }) => ({
      height: 40,
      minHeight: 40,
      paddingTop: 0,
      paddingBottom: 0,
      paddingLeft: 12,
      paddingRight: 12,
      borderRadius: 8,

      transition: theme.transitions.create(
        ["background-color", "padding"],
        { duration: 150 }
      ),

      "&.Mui-selected": {
        backgroundColor: theme.palette.iconButton.selected,

        "&:hover": {
          backgroundColor: theme.palette.iconButton.active,
        },
      },

      "&:hover": {
        backgroundColor: theme.palette.iconButton.hover,
      },
    }),
  },
};

export default MuiListItemButton;
