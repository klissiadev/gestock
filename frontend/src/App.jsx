import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import NotificationToast from "./features/notifications/components/NotificationToast";

function App() {
  return (
    <BrowserRouter>
      <NotificationToast />
      <AppRoutes />
    </BrowserRouter>
  )
}
export default App;

