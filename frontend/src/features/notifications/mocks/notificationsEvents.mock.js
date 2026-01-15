import { NOTIFICATION_TYPE } from "../constants/notificationType";

/** @type {import("../models/NotificationEvent.model").NotificationEvent[]} */
export const notificationEventsMock = [
  {
    // alerta de ruptura (estoque abaixo do limite)
    id: "evt-001",
    type: NOTIFICATION_TYPE.RUPTURE,
    context: {
      state: "BELOW_MINIMUM",
      data: {
        currentStock: 3,
        minimumStock: 10
      }
    },
    reference: {
      type: "PRODUCT",
      id: "PROD-001"
    },
    createdAt: "2026-01-10T10:00:00Z",
    userId: "USR-001"
  },
  {
    // alerta de ruptura (estoque perto do limite)
    id: "evt-002",
    type: NOTIFICATION_TYPE.RUPTURE,
    context: {
      state: "ISNEAR_MINIMUM",
      data:{
        currentStock: 18
      }
    },
    reference: {
      type: "PRODUCT",
      id: "PROD-002"
    },
    createdAt: "2026-01-11T10:00:00Z",
    userId: "USR-001"
  },
  {
    // alerta de produto próximo da validade
    id: "evt-003",
    type: NOTIFICATION_TYPE.VALIDITY,
    context: {
      state: "NEAR_EXPIRATION",
      data:{
        expirationDate: "2026-01-20"
      }
    },
    reference: {
      type: "PRODUCT",
      id: "PROD-004"
    },
    createdAt: "2026-01-10T09:10:00Z",
    userId: "USR-001"
  },
  {
    // alerta de produto vencido
    id: "evt-004",
    type: NOTIFICATION_TYPE.VALIDITY,
    context: {
      state: "EXPIRED",
      data:{
        expirationDate: "2026-01-10"
      }
    },
    reference: {
      type: "PRODUCT",
      id: "PROD-005"
    },
    createdAt: "2026-01-12T09:10:00Z",
    userId: "USR-001"
  },
  {
    // aviso de importação concluída
    id: "evt-005",
    type: NOTIFICATION_TYPE.SUCCESS,
    context: {
      state: "STOCK_UPDATED",
    },
    reference: {
      type: "IMPORT",
      id: "IMP-2026-01"
    },
    createdAt: "2026-01-10T08:45:00Z",
    userId: "USR-001"
  },
  {
    // informativo de sugestão
    id: "evt-006",
    type: NOTIFICATION_TYPE.SUGGESTION,
    context: {
      state: "SUGGEST_REPLENISHMENT",
      data:{
        suggestion: ""
      }
    },
    reference: {
      type: "PRODUCT",
      id: "PROD-005"
    },
    createdAt: "2026-01-10T08:45:00Z",
    userId: "USR-001"
  },
];
