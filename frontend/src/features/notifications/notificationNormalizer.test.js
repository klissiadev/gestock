import { getNotificationsMocked } from "../notifications/services/notificationService";


console.log("🧪 TESTE — Notification Service");

const notifications = getNotificationsMocked();

console.log("📢 NOTIFICAÇÕES GERADAS:");
console.table(notifications);
