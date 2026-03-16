const MuiTextField = {
  defaultProps: {
    variant: "outlined",
    size: "small",
    fullWidth: true,
  },

  styleOverrides: {
    root: {
      "& .MuiOutlinedInput-root": {
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

        "&.Mui-error fieldset": {
          borderColor: "#FF3B30",
        },
      },

      // altura fixa SOMENTE para inputs normais
      "& .MuiOutlinedInput-root:not(.MuiInputBase-multiline)": {
        height: 45,
      },

      "& .MuiOutlinedInput-input": {
        fontSize: "14px",
        padding: "10px 14px",
      },

      "& .MuiFormHelperText-root": {
        fontSize: 12,
        marginLeft: 0,
      },

      "& .MuiFormHelperText-root.Mui-error": {
        color: "#FF3B30",
      },

      "& .MuiInputLabel-root.Mui-error": {
        color: "#FF3B30",
      },

      "& .MuiOutlinedInput-root.Mui-error .MuiOutlinedInput-input::placeholder": {
        color: "#FF3B30",
        opacity: 1,
      },
    },
  },
};

export default MuiTextField;