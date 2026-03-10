import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from "../AuthContext"

export const ProtectedRoute = ({ allowedRoles }) => {
  const { user, loading } = useAuth();

  // Tela de carregamento
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
        Carregando sessão...
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.papel && !allowedRoles.includes(user.papel)) {
    if (user.papel === 'admin') {
      return <Navigate to="/debug2" replace />;
    } else if (user.papel === 'gestor') {
      return <Navigate to="/home" replace />;
    }
  }


  return <Outlet />;
};