import { Box } from "@mui/material";
import ExpandableIconButton from "../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../assets/icon/iconChat.svg?react";


export default function HomePage() {

  return (
    <Box display="flex" >
      {/* Conteúdo da página */}
      <Box flex={1} p={3}>
        <h1>Home Page</h1>
        <ExpandableIconButton
          icon={<ChatSvg width={20} height={20} />} 
          origin="home"
          initialMessage="Olá Minerva, me ajude na tela inicial."
        />
      </Box>
    </Box>
  );
}

