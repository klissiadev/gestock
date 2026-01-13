import { NOTIFICATION_TYPE } from "../constants/notificationType";
import { NOTIFICATION_SEVERITY } from "../constants/notificationSeverity";

/**
 * Modelo final de notificação (pronto para UI)
 */

/**
 * @typedef {Object} Notification
 *
 * @property {string} id
 * @property {NOTIFICATION_TYPE} type
 * @property {NOTIFICATION_SEVERITY} severity
 *
 * @property {string} title
 * @property {string} message
 *
 * @property {Object} reference
 * @property {"PRODUCT" | "STOCK" | "IMPORT"} reference.type
 * @property {string} reference.id
 *
 * @property {boolean} read
 * @property {string} createdAt
 * @property {string} userId
 */

export {};
