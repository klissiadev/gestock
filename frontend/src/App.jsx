import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import NotificationToast from "./features/notifications/components/NotificationToast";
import { AuthProvider } from "./AuthContext";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <NotificationToast />
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}
export default App;

