import { NOTIFICATION_TYPE } from "../constants/notificationType";

export const notificationsMock = [
  {
    id: "1",
    type: NOTIFICATION_TYPE.RUPTURE,
    title: "Risco de ruptura",
    message: " ",
    reference: {
      type: "PRODUCT",
      id: "PROD-001",
    },
    read: false,
    createdAt: "2026-01-10T10:00:00Z",
  },
  {
    id: "2",
    type: NOTIFICATION_TYPE.SUCCESS,
    title: "Estoque atualizado",
    message: " ",
    reference: {
      type: "IMPORT",
      id: "IMP-2026",
    },
    read: true,
    createdAt: "2026-01-10T09:30:00Z",
  },
  {
    id: "3",
    type: NOTIFICATION_TYPE.SUGGESTION,
    title: " ",
    message: " ",
    reference: {
      type: "PRODUCT",
      id: "IMP-2026",
    },
    read: true,
    createdAt: "2026-01-11T09:30:00Z",
  },
  {
    id: "4",
    type: NOTIFICATION_TYPE.VALIDITY,
    title:  " ",
    message: " ",
    reference: {
      type: "PRODUCT",
      id: "IMP-2026",
    },
    read: true,
    createdAt: "2026-01-11T09:30:00Z",
  },
];
