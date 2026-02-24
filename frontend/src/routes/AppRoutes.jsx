import { Routes, Route } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import TabelaProduto from '../features/stock/pages/TabelaProduto';
import UploadPage from '../features/upload/pages/UploadPage';
import NotificationPage from '../features/notifications/NotificationPage';
import LLMPage from '../features/LLM/LLMPage';
import ForecastPage from '../features/forecast/ForecastPage';
import ReportsPage from '../features/reports/ReportsPage';
import RequestsPage from '../features/requests/RequestsPage';
import UploadPageDebug from "../features/debug/UploadPageDebug";
import AlertDialogSlide from "../features/upload/components/SucessBox";
import TabelaMovimentacao from '../features/stock/pages/TabelaMovimentacao';
import StockSheets from "../features/stock/StockPageDebug";
import StockPage from '../features/stock/StockPageDebug';
import HomePage2 from "../features/home/copia";
import HomePage from "../features/home/HomePage";
import UploadDialog from "../features/upload/UploadDialog";
import RegisterUserPage from "../features/users/pages/RegisterUserPage";

import ForgotPassword from "../features/users/pages/ForgotPassword";
import ResetPassword from "../features/users/pages/ResetPassword";
import AdminPage from "../features/admin/AdminPage";
import LoginPage from "../features/auth/pages/LoginPage";
import UsersPage from "../features/users/pages/ManageUsersPage";
import { ProtectedRoute } from "./ProtectedRoute";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path='/' element={<LoginPage />} />
      <Route path='/login' element={<LoginPage />} />
      <Route path='/register-user' element={<RegisterUserPage/>}/>
      <Route path="/reset-password" element={<ResetPassword/>}/> 
      <Route path="/forgot-password" element={<ForgotPassword/>}/>
      <Route path="/users" element={<UsersPage/>}/> 
      <Route element={
        <ProtectedRoute>
          <AppLayout />
        </ProtectedRoute>
      }>
        <Route path='/home' element={<HomePage2 />} />
        <Route path='/upload' element={<UploadDialog />} />
        <Route path='/sheets' element={<TabelaProduto />} />
        <Route path='/notifications' element={<NotificationPage />} />
        <Route path="/movements" element={<TabelaMovimentacao />} />
        <Route path='/ai' element={<LLMPage />} />
        <Route path='/forecast' element={<ForecastPage />} />
        <Route path='/reports' element={<ReportsPage />} />
        <Route path='/requests' element={<RequestsPage />} />
        <Route path='/debug' element={<StockSheets />} />
        <Route path='/debug2' element={<AdminPage />} />

      </Route>
    </Routes>
  )
}

export default AppRoutes