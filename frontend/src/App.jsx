import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import NotificationToastTester from "./features/notifications/components/NotificationItem";

function App() {
  return (
    <BrowserRouter>
      <NotificationToastTester />
      <AppRoutes />
    </BrowserRouter>
  )
}
export default App;

