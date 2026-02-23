import { Box, Typography } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

const STEPS = [
  { id: 1, label: "Dados Pessoais" },
  { id: 2, label: "Criar senha" },
  { id: 3, label: "Concluído" },
];

export default function StepProgress({ activeStep = 1 }) {
  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="center"
      mt={3}
    >
      {STEPS.map((step, index) => {
        const isCompleted = activeStep > step.id;
        const isActive = activeStep === step.id;
        const isFuture = activeStep < step.id;

        return (
          <Box key={step.id} display="flex" alignItems="center">
            {/* STEP ITEM */}
            <Box display="flex" alignItems="center" gap={1}>
              {/* CIRCLE / CHECK */}
              {isCompleted ? (
                <CheckCircleIcon
                  sx={{
                    fontSize: 20,
                    color: (theme)=> theme.palette.background.default,
                }}
                />
              ) : (
                <Box
                  sx={(theme) => ({
                    width: isFuture ? 17 : 18,
                    height: isFuture ? 17 : 18,
                    borderRadius: "50%",
                    backgroundColor: isCompleted || isActive
                    ?  theme.palette.background.default
                    :  theme.palette.card.background,
                  })}
                />
              )}

              {/* LABEL */}
              <Typography
                fontSize={16}
                sx={{
                  fontWeight: 500,
                  color: isFuture
                    ? "text.disabled"
                    : "text.primary",
                }}
              >
                {step.id.toString().padStart(2, "0")} {step.label}
              </Typography>
            </Box>

            {/* LINE */}
            {index < STEPS.length - 1 && (
              <Box
                sx={{
                  width: 40,
                  height: 3,
                  mx: 2,
                  backgroundColor: "divider",
                }}
              />
            )}
          </Box>
        );
      })}
    </Box>
  );
}
