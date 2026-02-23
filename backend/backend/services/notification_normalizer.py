from typing import Optional, Dict, Any
from backend.database.schemas import NotificationCreate
from backend.database.schemas import (
    NotificationSeverity,
    NotificationEventType
)
from datetime import datetime, date

# função para calcular número de dias
def days_until(data_alvo: str) -> int:
    """
    data_alvo deve estar no formato 'YYYY-MM-DD'
    """
    today = date.today()
    target = datetime.strptime(data_alvo, "%Y-%m-%d").date()

    diff_dias = (target - today).days

    return diff_dias


def normalize_event(evento: dict) -> Optional[NotificationCreate]:
    """
    Recebe um evento bruto e retorna uma notificação pronta
    ou None se o evento não gerar notificação.
    """

    event_type = evento["type"]
    context = evento["context"]
    reference = evento["reference"]

    state = context.get("state")
    data = context.get("data", {})

    base = {
        "type": event_type,
        "reference": reference,
        "event_id": evento["id"],
        "user_id": evento["user_id"],
    }

    # ======================
    # RUPTURE
    # ======================
    if event_type == "RUPTURE":

        if state == "BELOW_MINIMUM":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.CRITICAL,
                title="Estoque abaixo do mínimo",
                message=(
                    f"O produto {reference['nome']} possui apenas "
                    f"{data.get('currentStock')} unidades em estoque."
                ),
            )

        if state == "NEAR_MINIMUM":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.WARNING,
                title="Estoque próximo do mínimo",
                message=(
                    f"O produto {reference['nome']} está próximo do limite mínimo de {data.get('minimumStock')} unidades"
                ),
            )

    # ======================
    # SUCCESS
    # ======================

    if event_type == "SUCCESS" and state == "IMPORT_SUCCESS":
        return NotificationCreate(
            **base,
            severity=NotificationSeverity.SUCCESS,
            title="Importação concluída",
            message=f"A importação {reference['id']} foi finalizada com sucesso.",
        )
    
    # ======================
    # VALIDITY
    # ======================

    if event_type == "VALIDITY" :
        if state == "EXPIRED":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.CRITICAL,
                title="Produto vencido",
                message=f"O produto {reference['nome']} está vencido há {(-1)*days_until(data.get('expirationDate'))} dias."
            )
        
        if state == "NEAR_EXPIRATION":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.WARNING,
                title="Produto próximo do vencimento",
                message=f"O produto {reference['nome']} vencerá em {(-1)*days_until(data.get('expirationDate'))} dias."
            )

    # ======================
    # ERROR
    # ======================
    if event_type == "ERROR" and state == "ERROR":
        return NotificationCreate(
            **base,
            severity=NotificationSeverity.CRITICAL,
            title="Erro encontrado",
            message=f"{data.get('error')}"
        )
    
    # ======================
    # SUGGESTION
    # ======================
    if event_type == "SUGGESTION" and state == "SUGGEST_REPLENISHMENT":
        return NotificationCreate(
            **base,
            severity=NotificationSeverity.INFO,
            title="Sugestão de demanda",
            message=f"Melhor momento para repor o produto {reference['nome']}, veja porque..."
        )

    # ======================
    # EVENTO SEM NOTIFICAÇÃO
    # ======================
    return None
