import React from 'react'
import ExpandableIconButton from "../../components/ui/ExpandableIconButton.jsx";
import ChatSvg from "../../assets/icon/iconChat.svg?react";

const RequestsPage = () => {
  return (
    <div>RequestsPage
      <ExpandableIconButton
        icon={<ChatSvg width={20} height={20} />} 
        origin="requests"
        initialMessage="Olá Minerva, me ajude na tela de solicitações."
      />
    </div>
  )
}

export default RequestsPage