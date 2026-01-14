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

// função para calcular número de dias
function daysUntil(dataAlvo) {
  const today = new Date();
  const target = new Date(dataAlvo);

  // Zera horas para evitar erro de fuso/horário
  today.setHours(0, 0, 0, 0);
  target.setHours(0, 0, 0, 0);

  const diffMs = target - today;
  const diffDias = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

  return diffDias;
}

export function normalizeNotification(event) {
  const { type, context, reference, createdAt, userId, id } = event;
  const { flags, data } = context;

  // RUPTURA
  if (type === "RUPTURE") {
    if (event.context.state === "BELOW_MINIMUM") {
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

    if (event.context.state === "ISNEAR_MINIMUM") {
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
    if(event.context.state === "IS_EXPIRED"){
        return baseNotification({
            id,
            type,
            severity: NOTIFICATION_SEVERITY.CRITICAL,
            title: "Lote vencido",
            message: `O produto ${reference.id} está vencido há ${(-1)*daysUntil(data?.expirationDate)} dias.`,
            reference,
            createdAt,
            userId
        })
    }

    if(event.context.state === "ISNEAR_EXPIRATION"){
        return baseNotification({
            id,
            type,
            severity: NOTIFICATION_SEVERITY.WARNING,
            title: "Lote próximo do vencimento",
            message: `O produto ${reference.id} vencerá em ${daysUntil(data?.expirationDate)} dias.`,
            reference,
            createdAt,
            userId
        })
    }
  }
  //SUCCESS
  if (type === "VALIDITY" && event.context.state === "STOCK_UPDATED"){
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
    if(type === "SUGGESTION" && event.context.state === "SUGGEST_REPLENISHMENT"){
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