import React from 'react'
import { Route, Routes } from 'react-router-dom'
import StockSheets from '../pages/StockSheets'
import UploadPage from '../pages/UploadPage'


const AppRoutes = () => {
  return (
    <Routes>
        <Route path='/' element={<UploadPage />}/>
        <Route path='/sheets' element={<StockSheets />}/>
    </Routes>
  )
}

export default AppRoutes
