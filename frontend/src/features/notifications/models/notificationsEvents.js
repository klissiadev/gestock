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
 * @property {Object} [context.data]
 * @property {number} [context.data.currentStock]
 * @property {number} [context.data.minimumStock]
 * @property {string} [context.data.expirationDate]
 * @property {string} [context.data.suggestion]
 * @property {string} [context.data.error]
 *
 * @property {Object} reference
 * @property {"PRODUCT" | "STOCK" | "IMPORT"} reference.type
 * @property {string} reference.id
 *
 * @property {string} createdAt
 * @property {string} userId
 */

export {};
