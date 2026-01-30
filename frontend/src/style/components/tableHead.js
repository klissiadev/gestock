export const MuiTableHead = {
    styleOverride: {
        root : ({ theme }) => ({
            textAlign: "center",
            fontFamily:theme.typography.fontFamily,
            fontWeight: theme.typography.fontWeightBold,
            borderBottom:`1px solid ${theme.palette.common.black}`,
            backgroundColor: theme.palette.table.main,
            tableLayout: "fixed",
        }),
    }

};