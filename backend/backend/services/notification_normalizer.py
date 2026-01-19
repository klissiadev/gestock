from typing import Optional, Dict, Any
from backend.database.schemas import NotificationCreate
from backend.database.schemas import (
    NotificationSeverity,
    NotificationEventType
)

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
                    f"O produto {data.get('produto')} possui apenas "
                    f"{data.get('estoque_atual')} unidades em estoque."
                ),
            )

        if state == "ISNEAR_MINIMUM":
            return NotificationCreate(
                **base,
                severity=NotificationSeverityState.WARNING,
                title="Estoque próximo do mínimo",
                message=(
                    f"O produto {data.get('produto')} está próximo do limite mínimo."
                ),
            )

    # ======================
    # IMPORT / SUCCESS
    # ======================
    if event_type == "IMPORT" and state == "SUCCESS":
        return NotificationCreate(
            **base,
            severity=NotificationSeverityState.INFO,
            title="Importação concluída",
            message=f"A importação {reference['id']} foi finalizada com sucesso.",
        )

    # ======================
    # EVENTO SEM NOTIFICAÇÃO
    # ======================
    return None
