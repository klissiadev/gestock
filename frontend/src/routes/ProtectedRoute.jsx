import { Navigate } from "react-router-dom";
import { useAuth } from "../AuthContext"

export const ProtectedRoute = ({ children }) => {
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
    return <Navigate to="/" />;
  }

  return children;
};