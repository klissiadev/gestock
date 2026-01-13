import { notificationEventsMock } from "../mocks/notificationsEvents.mock";
import { normalizeNotification } from "./notificationNormalizer";

export function getNotificationsMocked() {
  return notificationEventsMock
    .map(normalizeNotification)
    .filter(Boolean);
}
