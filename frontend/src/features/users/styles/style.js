import { height, width } from "@mui/system";

export const accept_button = {
    flex: 1,
    borderRadius: 3,
    height: 40,
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
    height: 40,
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
