// textField.jsx
const MuiInput = {

  styleOverrides: {
    root: ({ theme }) => ({
      // remove qualquer underline azul
      "&:before": {
        border: "none",
      },
      "&:hover:not(.Mui-disabled):before": {
        border: "none",
      },
      "&:after": {
        border: "none",
      },
    }),
  },
};

export default MuiInput;
