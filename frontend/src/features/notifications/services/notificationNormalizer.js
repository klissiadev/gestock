import { NOTIFICATION_SEVERITY } from "../constants/notificationSeverety";

// Serviço que estrutura os eventos em mensagens prontas para notificação e alertas

/**
 * @param {import("../models/NotificationEvent.model").NotificationEvent} event
 */

function baseNotification({
  id,
  type,
  severity,
  title,
  message,
  reference,
  createdAt
}) {
  return {
    id,
    type,
    severity,
    title,
    message,
    reference,
    createdAt,
    read: false
  };
}

export function normalizeNotification(event) {
  const { type, context, reference, createdAt, userId, id } = event;
  const { flags, data } = context;

  // RUPTURA
  if (type === "RUPTURE") {
    if (flags.isBelowMinimum) {
      return baseNotification({
        id,
        type,
        severity: NOTIFICATION_SEVERITY.CRITICAL,
        title: "Estoque abaixo do mínimo",
        message: `O produto ${reference.id} possui apenas ${data?.currentStock} unidades em estoque.`,
        reference,
        createdAt,
        userId
      });
    }

    if (flags.isNearMinimum) {
      return baseNotification({
        id,
        type,
        severity: NOTIFICATION_SEVERITY.WARNING,
        title: "Estoque próximo do mínimo",
        message: `O produto ${reference.id} está próximo do limite mínimo. Com apenas ${data?.currentStock} unidades em estoque.`,
        reference,
        createdAt,
        userId
      });
    }
  }
  //VALIDADE 
  if (type === "VALIDITY"){
    if(flags.isExpired){
        return baseNotification({
            id,
            type,
            severity: NOTIFICATION_SEVERITY.CRITICAL,
            title: "Lote vencido",
            message: `O produto ${reference.id} está vencido desde o dia ${data?.expirationDate}.`,
            reference,
            createdAt,
            userId
        })
    }

    if(flags.isNearExpiration){
        return baseNotification({
            id,
            type,
            severity: NOTIFICATION_SEVERITY.WARNING,
            title: "Lote próximo do vencimento",
            message: `O produto ${reference.id} vencerá dia ${data?.expirationDate}.`,
            reference,
            createdAt,
            userId
        })
    }
  }
  //SUCCESS
  if (type === "VALIDITY" && flags.importCompleted && flags.stockUpdated){
        return baseNotification({
            id,
            type,
            severity: NOTIFICATION_SEVERITY.SUCCESS,
            title: "Novas movimentações adicionadas",
            message: `Nova importação ${reference.id} realizada, estoque atualizado.`,
            reference,
            createdAt,
            userId
        })
    }
    //ERROR
    if(type === "ERROR" && flags.hasInconsistency){
        return baseNotification({
            id,
            type,
            severity: NOTIFICATION_SEVERITY.CRITICAL,
            title: "Erro encontrado",
            message: `${data?.error}`,
            reference,
            createdAt,
            userId
        })
    }
    //SUGGESTION
    if(type === "SUGGESTION" && flags.suggestReplenishment){
        return baseNotification({
            id,
            type,
            severity: NOTIFICATION_SEVERITY.INFO,
            title: "Sugestão de demanda",
            message: `Melhor momento para repor o produto ${reference.id}, veja porque...`,
            reference,
            createdAt,
            userId
        })
    }

    return null;
}