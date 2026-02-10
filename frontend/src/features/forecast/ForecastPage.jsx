import React from 'react'
import ExpandableIconButton from "../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../assets/icon/iconChat.svg?react";

const ForecastPage = () => {
  return (
    <div>ForecastPage
      <ExpandableIconButton
        icon={<ChatSvg width={20} height={20} />} 
        origin="forecast"
        initialMessage="Olá Minerva, me ajude na tela de previsão."
      />
    </div>
  )
}

export default ForecastPage