import { Routes, Route } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import TabelaProduto from '../features/stock/pages/TabelaProduto';
import NotificationPage from '../features/notifications/NotificationPage';
import LLMPage from '../features/LLM/LLMPage';
import ForecastPage from '../features/forecast/ForecastPage';
import ReportsPage from '../features/reports/ReportsPage';
import RequestsPage from '../features/requests/RequestsPage';
import TabelaMovimentacao from '../features/stock/pages/TabelaMovimentacao';
import StockSheets from "../features/stock/StockPageDebug";
import HomePage2 from "../features/home/copia";
import UploadDialog from "../features/upload/UploadDialog";
import RegisterUserPage from "../features/users/pages/RegisterUserPage";

import ForgotPassword from "../features/users/pages/ForgotPassword";
import ResetPassword from "../features/users/pages/ResetPassword";
import AdminPage from "../features/admin/AdminPage";
import LoginPage from "../features/auth/pages/LoginPage";
import UsersPage from "../features/users/pages/ManageUsersPage";
import { ProtectedRoute } from "./ProtectedRoute";

import { useAuth } from "../AuthContext";

const AppRoutes = () => {
  const { user } = useAuth();
  const isAdmin = user?.papel === 'admin';


  return (
    <Routes>
      <Route path='/' element={<LoginPage />} />
      <Route path='/login' element={<LoginPage />} />
      <Route path='/register-user' element={<RegisterUserPage />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/users" element={<UsersPage />} />

      <Route element={
        <ProtectedRoute>
          <AppLayout isAdmin={isAdmin} />
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

      {isAdmin && (
        <>
          <Route path='/debug2' element={<AdminPage />} />
        </>
      )}
    </Routes>
  )
}

export default AppRoutes