import { minHeight } from "@mui/system";

// src/style/components/listItemIcon.js
const MuiListItemIcon = {
  styleOverrides: {
    root: {
      minWidth: 0,
      marginRight: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      minHeight: 0,

      "& svg": {
        fontSize: 18,
      },
    },
  },
};

export default MuiListItemIcon;
