export const MuiPaper = {
  variants: [
    {
      props: { variant: 'errorContainer' },
      style: ({ theme }) => ({
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: theme.spacing(8),
        backgroundColor: theme.palette.errors.background,
        border: `1px dashed ${theme.palette.errors.border}`,
        borderRadius: theme.shape.borderRadius * 2,
        boxShadow: 'none', // Remove a sombra padrão do Paper
      }),
    },
  ],
};