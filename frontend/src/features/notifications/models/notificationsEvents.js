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
 * @property {Object} context.flags
 *
 * // Ruptura / estoque
 * @property {boolean} [context.flags.isBelowMinimum]
 * @property {boolean} [context.flags.isNearMinimum]
 *
 * // Validade
 * @property {boolean} [context.flags.isExpired]
 * @property {boolean} [context.flags.isNearExpiration]
 *
 * // Sucesso
 * @property {boolean} [context.flags.importCompleted]
 * @property {boolean} [context.flags.stockUpdated]
 *
 * // Erro
 * @property {boolean} [context.flags.hasInconsistency]
 * 
 * // Sugestão
 * @property {boolean} [context.flags.suggestReplenishment]
 *
 * @property {Object} [context.data]
 * @property {number} [context.data.currentStock]
 * @property {number} [context.data.minimumStock]
 * @property {string} [context.data.expirationDate]
 *
 * @property {Object} reference
 * @property {"PRODUCT" | "STOCK" | "IMPORT"} reference.type
 * @property {string} reference.id
 *
 * @property {string} createdAt
 * @property {string} userId
 */

export {};
