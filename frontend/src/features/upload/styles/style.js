export const stack_principal = {
    backgroundColor: (theme) => theme.palette.common.white,
    width: "100%",
    padding: 1,
    textAlign: "center",
};

export const typeSelector = {
    backgroundColor: (theme) => theme.palette.uploadBox.main,
    textAlign: 'start',
    borderStyle: "solid",
    borderWidth: "1px",
    borderRadius: 3,
    borderColor: (theme) => theme.palette.common.black,
    "& .MuiOutlinedInput-notchedOutline": {
        border: "none",
    },
    "&:hover .MuiOutlinedInput-notchedOutline": {
        border: "none",
    },
    "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
        border: "none",
    },
};

export const menuItem = {
    fontFamily: theme => theme.typography.fontFamily,
    fontWeight: theme => theme.typography.fontWeightRegular,
}

export const dragBox = {
    borderStyle: "dashed",
    borderWidth: "2px",
    borderRadius: 4,
    borderColor: (theme) => theme.palette.button.main,
    padding: 10,
};

export const uploadText = {
    fontFamily: (theme) => theme.typography.fontFamily,
    fontWeight: (theme) => theme.typography.fontWeightLight,
    textAlign: "center",
};

export const accept_button = {
    flex: 1,
    borderRadius: 3,
    fontFamily: (theme) => theme.typography.fontFamily,
    fontWeight: (theme) => theme.typography.fontWeightLight,
    color: theme => theme.palette.common.white,
    backgroundColor: (theme) => theme.palette.uploadBox.button,
    "&:hover": {
        backgroundColor: (theme) => theme.palette.button.hover,
        color: theme => theme.palette.common.black,
    },
    textTransform: "none",
};

export const cancel_button = {
    flex: 1,
    borderRadius: 3,
    fontFamily: (theme) => theme.typography.fontFamily,
    fontWeight: (theme) => theme.typography.fontWeightLight,
    backgroundColor: (theme) => theme.palette.uploadBox.main,
    "&:hover": {
        backgroundColor: (theme) => theme.palette.button.hover,
        color: theme => theme.palette.common.black,
    },
    textTransform: "none",
    borderStyle: "solid",
    borderWidth: "1px",
    borderColor: (theme) => theme.palette.common.black,

};

export const button_model = {
    whiteSpace: "nowrap",
    width: "fit-content",
    paddingX: 5,
    backgroundColor: (theme) => theme.palette.uploadBox.button,
    "&:hover": {
        backgroundColor: (theme) => theme.palette.background.default,
    },
    fontFamily: (theme) => theme.typography.fontFamily,
    fontWeight: (theme) => theme.typography.fontWeightBold,
    color: theme => theme.palette.common.white,
    textTransform: "none",
    borderRadius: 3
}

export const paper_box = {
    backgroundColor: theme => theme.palette.uploadBox.main,
    maxWidth: 500,
    p: 4,
    borderRadius: 3,
    boxShadow: 3,
    height: "fit-content",
    m: "auto"
}