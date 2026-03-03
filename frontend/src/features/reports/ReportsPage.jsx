import React from 'react'
import ExpandableIconButton from "../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../assets/icon/iconChat.svg?react";

const ReportsPage = () => {
  return (
    <div>ReportsPage

      <ExpandableIconButton
        icon={<ChatSvg width={20} height={20} />} 
        origin="reports"
        initialMessage="Olá Minerva, me ajude na tela de relatórios."
      />
    </div>
  )
}

export default ReportsPage