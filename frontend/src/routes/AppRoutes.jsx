import React from 'react'
import {Routes, Route } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import StockSheets from '../features/stock/pages/StockSheets';
import UploadPage from '../features/upload/pages/UploadPage';
import NotificationPage from '../features/notifications/NotificationPage';
import LLMPage from '../features/llm/pages/LLMPage';
import HomePage from '../features/home/HomePage';
import ForecastPage from '../features/forecast/ForecastPage';
import ReportsPage from '../features/reports/ReportsPage';
import RequestsPage from '../features/requests/RequestsPage';
import StockPage from '../features/stock/StockPage';

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path='/' element={<HomePage/>}/>
        <Route path='/upload' element={<UploadPage />}/>
        <Route path='/sheets' element={<StockSheets />}/>
        <Route path='/notifications' element={<NotificationPage/>}/>
        <Route path='/ai' element={<LLMPage/>}/>
        <Route path='/forecast' element={<ForecastPage/>}/>
        <Route path='/reports' element={<ReportsPage/>}/>
        <Route path='/requests' element={<RequestsPage/>}/>
        <Route path='/debug' element={<StockPage />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes