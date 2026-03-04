import {
  fetchAllNotifications,
  fetchUnreadNotifications,
} from "./notificationApi";

export async function getUnreadNotifications(limit = 5, cursor = null) {
  const data = await fetchUnreadNotifications(limit, cursor);
  return data;
}

export async function getAllNotifications(limit = 20, cursor = null) {
  const data = await fetchAllNotifications(limit, cursor);
  return data;
}