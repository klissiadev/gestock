const MuiTextField = {
  defaultProps: {
    variant: "outlined",
    size: "small",
    fullWidth: true,
  },

  styleOverrides: {
    root: {
      "& .MuiOutlinedInput-root": {
        height: 45,
        borderRadius: 8,

        "& fieldset": {
          borderColor: "#969696",
        },

        "&:hover fieldset": {
          borderColor: "#bbb",
        },

        "&.Mui-focused fieldset": {
          borderColor: "#919191", 
        },
      },

      "& .MuiOutlinedInput-input": {
        fontSize: "14px",
        padding: "10px 14px",
      },
    },
  },
};

export default MuiTextField;
