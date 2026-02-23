import { Box, Typography, Chip } from "@mui/material";
import LampSvg from "../../../assets/icon/iconLamp.svg?react";

const suggestions = [
  "Como gerar um relatório?",
  "Quais dados posso consultar?",
  "Como integrar com o sistema?",
  "Tenho um erro no processo",
];

const FAQSuggestions = ({ onSelectSuggestion }) => {
  return (
    <Box sx={{ mt: 3 , width:'100%'}}>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <LampSvg style={{ width: 16, height: 16}} />  
        <Typography
          color="black"
          sx={{ display: "block" }}
          fontSize={14}
        >
          Dúvidas frequentes
        </Typography>
      </Box>

      <Box
        display="flex"
        flexWrap="wrap"
        gap={1}
        justifyContent="center"
      >
        {suggestions.map((text, idx) => (
          <Box
            key={idx}
            sx={{
              flexBasis: "calc(50% - 4px)",
            }}
          >
            <Chip
              label={text}
              onClick={() => onSelectSuggestion(text)}
              sx={{ width: "100%", borderRadius: 2, cursor: "pointer" }}
            />
          </Box>
        ))}
      </Box>

    </Box>
  );
};

export default FAQSuggestions;
