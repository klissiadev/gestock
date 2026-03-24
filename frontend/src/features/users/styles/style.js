

export const accept_button = {
    flex: 1,
    borderRadius: 3,
    height: 40,
    fontFamily: (theme) => theme.typography.fontFamily,
    fontWeight: (theme) => theme.typography.fontWeightLight,
    color: theme => theme.palette.common.white,
    backgroundColor: (theme) => theme.palette.primary.main,
    "&:hover": {
        backgroundColor: (theme) => theme.palette.button.hover,
        color: theme => theme.palette.common.black,
    },
    textTransform: "none",
    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.16)",
};

export const cancel_button = {
    flex: 1,
    borderRadius: 3,
    height: 40,
    fontFamily: (theme) => theme.typography.fontFamily,
    fontWeight: (theme) => theme.typography.fontWeightLight,
    backgroundColor: "none",
    "&:hover": {
        backgroundColor: (theme) => theme.palette.button.hover,
        color: theme => theme.palette.common.black,
    },
    textTransform: "none",
    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.16)",
};
