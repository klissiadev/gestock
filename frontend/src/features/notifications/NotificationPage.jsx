import { useNotifications } from "../../hooks/useNotifications";
import { NotificationList } from "./components/NotificationList";

const NotificationPage = () => {
  const { notifications, loading } = useNotifications();

  if (loading) return <p>Carregando...</p>;

  return <NotificationList notifications={notifications} />;
};

export default NotificationPage;
