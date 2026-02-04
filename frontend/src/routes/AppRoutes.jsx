import { Routes, Route } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import TabelaProduto from '../features/stock/pages/TabelaProduto';
import UploadPage from '../features/upload/pages/UploadPage';
import NotificationPage from '../features/notifications/NotificationPage';
import LLMPage from '../features/LLM/LLMPage';
import HomePage from '../features/home/HomePage';
import ForecastPage from '../features/forecast/ForecastPage';
import ReportsPage from '../features/reports/ReportsPage';
import RequestsPage from '../features/requests/RequestsPage';
import UploadPageDebug from "../features/upload/UploadPageDebug";

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path='/' element={<HomePage/>}/>
        <Route path='/sheets' element={<TabelaProduto />}/>
        <Route path='/notifications' element={<NotificationPage/>}/>
        <Route path='/ai' element={<LLMPage/>}/>
        <Route path='/forecast' element={<ForecastPage/>}/>
        <Route path='/reports' element={<ReportsPage/>}/>
        <Route path='/requests' element={<RequestsPage/>}/>
        <Route path='/upload' element={<UploadPageDebug />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes