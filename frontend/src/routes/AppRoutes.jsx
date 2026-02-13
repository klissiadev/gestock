import { Routes, Route } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import TabelaProduto from '../features/stock/pages/TabelaProduto';
import UploadPage from '../features/upload/pages/UploadPage';
import NotificationPage from '../features/notifications/NotificationPage';
import LLMPage from '../features/LLM/LLMPage';
import ForecastPage from '../features/forecast/ForecastPage';
import ReportsPage from '../features/reports/ReportsPage';
import RequestsPage from '../features/requests/RequestsPage';
import UploadPageDebug from "../features/upload/UploadPageDebug";
import AlertDialogSlide from "../features/upload/components/SucessBox";
import TabelaMovimentacao from '../features/stock/pages/TabelaMovimentacao';
import StockSheets from "../features/stock/StockPageDebug";
import StockPage from '../features/stock/StockPageDebug';
import HomePage2 from "../features/home/copia";
import HomePage from "../features/home/HomePage";

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path='/' element={<HomePage2/>}/>
        <Route path='/upload' element={<UploadPage />}/>
        <Route path='/sheets' element={<TabelaProduto />}/>
        <Route path='/notifications' element={<NotificationPage/>}/>
        <Route path='/ai' element={<LLMPage/>}/>
        <Route path='/forecast' element={<ForecastPage/>}/>
        <Route path='/reports' element={<ReportsPage/>}/>
        <Route path='/requests' element={<RequestsPage/>}/>
        <Route path='/debug' element={<StockSheets />} />
        <Route path='/debug2' element={<AlertDialogSlide />} />
        <Route path='/debug' element={<StockPage />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes