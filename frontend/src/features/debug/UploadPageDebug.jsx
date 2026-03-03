
import React, { useState, useEffect, useRef } from 'react';
import { CircularProgress, Stack, Typography, Fade } from '@mui/material';

export const frasesMinerva = {
  // Estágio 1: Resposta imediata
  curto: [
    "Pensando...",
    "Analisando...",
    "Buscando...",
    "Conectando...",
    "Ouvindo você..."
  ],
  
  // Estágio 2: Processamento moderado 
  medio: [
    "Cruzando informações...",
    "Mergulhando nos dados...",
    "Refinando o raciocínio...",
    "Consultando minha base...",
    "Organizando as ideias..."
  ],
  
  // Estágio 3: Respostas complexas
  longo: [
    "Essa é complexa! Só mais um instante...",
    "Caprichando na resposta...",
    "Quase pronto, estou finalizando...",
    "Ainda estou aqui, polindo os detalhes...",
    "Obrigada pela paciência, estou terminando!"
  ]
};


const LoadingComponent = () => {
    const [frase, setFrase] = useState(frasesMinerva.curto[0]);
    const [show, setShow] = useState(true);
    const segundosRef = useRef(0);

    useEffect(() => {
        const interval = setInterval(() => {
            segundosRef.current += 3; // Avançamos de 3 em 3 segundos
            
            const segundos = segundosRef.current;
            let categoria;

            if (segundos < 4) categoria = frasesMinerva.curto;
            else if (segundos < 9) categoria = frasesMinerva.medio;
            else categoria = frasesMinerva.longo;

            const novaFrase = categoria[Math.floor(Math.random() * categoria.length)];
            
            // Pequeno truque para o efeito de fade: esconde, muda o texto e mostra
            setShow(false);
            setTimeout(() => {
                setFrase(novaFrase);
                setShow(true);
            }, 300); // Tempo da transição

        }, 3000); // Troca a cada 3 segundos

        // LIMPEZA: Isso evita problemas de performance se o componente for destruído
        return () => clearInterval(interval);
    }, []);

    return (
        <Stack direction="row" alignItems="center" spacing={2} sx={{ minHeight: '40px' }}>
            <CircularProgress size={20} />
            <Fade in={show} timeout={300}>
                <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 500 }}>
                    {frase}
                </Typography>
            </Fade>
        </Stack>
    );
}




const UploadPageDebug = () => {
  return (
    <Stack
      direction="column"
      spacing={2}
      alignItems="center"
    >
      <LoadingComponent />

    </Stack>
  );
};

export default UploadPageDebug;
