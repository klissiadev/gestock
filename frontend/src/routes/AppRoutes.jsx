import React from 'react'
import { Route, Routes } from 'react-router-dom'

import StockSheets from '../features/estoque/pages/StockSheets'
import UploadPage from '../features/upload/pages/UploadPage'
import LLMPage from '../features/LLM/pages/LLMPage'

const AppRoutes = () => {
  return (
    <Routes>
      <Route path='/' element={<UploadPage />} />
      <Route path='/sheets' element={<StockSheets />} />
      <Route path='/llm' element={<LLMPage />} />
    </Routes>
  )
}

export default AppRoutes