import React from 'react'
import { Route, Routes } from 'react-router-dom'
import StockSheets from '../features/stock/pages/StockSheets'
import UploadPage from '../features/upload/pages/UploadPage'
import NotificationPage from '../features/notifications/NotificationPage'
import HomePage from '../features/home/HomePage'


const AppRoutes = () => {
  return (
    <Routes>
        <Route path='/' element={<HomePage/>}/>
        <Route path='/upload' element={<UploadPage />}/>
        <Route path='/sheets' element={<StockSheets />}/>
        <Route path='/notifications' element={<NotificationPage/>}/>
    </Routes>
  )
}

export default AppRoutes