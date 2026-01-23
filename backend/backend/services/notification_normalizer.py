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
    event_type = evento.get("type")
    context = evento.get("context", {})
    reference = evento.get("reference", {})

    state = context.get("state")
    data = context.get("data", {})

    base = {
        "type": event_type,
        "reference": reference,
        "event_id": evento.get("id"),
        "user_id": evento.get("user_id"),
    }

    nome = reference.get("nome", "produto")

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
                    f"O produto {nome} possui apenas "
                    f"{data.get('currentStock')} unidades em estoque."
                ),
            )

        if state == "NEAR_MINIMUM":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.WARNING,
                title="Estoque próximo do mínimo",
                message=(
                    f"O produto {nome} está próximo do limite mínimo "
                    f"de {data.get('minimumStock')} unidades"
                ),
            )

    # ======================
    # SUCCESS
    # ======================
    if event_type == "SUCCESS" and state == "IMPORT_SUCCESS":
        return NotificationCreate(
            **base,
            severity=NotificationSeverity.SUCCESS,
            title="Importação realizada",
            message=f"A importação {data.get('file_name')} foi finalizada com sucesso. Estoque atualizado.",
        )

    # ======================
    # VALIDITY
    # ======================
    if event_type == "VALIDITY":
        exp_date = data.get("expirationDate")
        if not exp_date:
            return None

        dias = days_until(exp_date)

        if state == "EXPIRED":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.CRITICAL,
                title="Produto vencido",
                message=f"O produto {nome} está vencido há {abs(dias)} dias."
            )

        if state == "NEAR_EXPIRATION":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.WARNING,
                title="Produto próximo do vencimento",
                message=f"O produto {nome} vencerá em {dias} dias."
            )

    # ======================
    # ERROR
    # ======================
    if event_type == "ERROR" and state == "ERROR":
        return NotificationCreate(
            **base,
            severity=NotificationSeverity.CRITICAL,
            title="Erro encontrado",
            message=data.get("error", "Erro desconhecido.")
        )

    # ======================
    # SUGGESTION
    # ======================
    if event_type == "SUGGESTION" and state == "SUGGEST_REPLENISHMENT":
        return NotificationCreate(
            **base,
            severity=NotificationSeverity.INFO,
            title="Sugestão de demanda",
            message=(
                f"Melhor momento para repor o produto {nome}. "
                f"Confira os detalhes no painel."
            )
        )

    return None
