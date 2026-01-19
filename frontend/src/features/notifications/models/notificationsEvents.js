// frontend/src/features/models/notificationEvents.model.js
import { NOTIFICATION_TYPE } from "../constants/notificationType";

/**
 * Modelo de evento bruto (fato do sistema).
 * Esse model NÃO tem título, mensagem ou urgência.
 * Ele será normalizado depois.
 */

/**
 * @typedef {Object} NotificationEvent
 *
 * @property {string} id
 * @property {NOTIFICATION_TYPE} type
 *
 * @property {Object} context
 * 
 * @property {string} context.state
 *
 * @property {Object<string, any>} [context.data]
 *
 * @property {Object} reference
 * @property {"PRODUCT" | "STOCK" | "IMPORT"} reference.type
 * @property {string} reference.id
 *
 * @property {string} createdAt
 * @property {string} userId
 */

export {};
