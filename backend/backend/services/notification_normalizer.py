import json
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

    context = evento.get("context")
    if isinstance(context, str):
        context = json.loads(context)
    context = context or {}

    reference = evento.get("reference")
    if isinstance(reference, str):
        reference = json.loads(reference)
    reference = reference or {}

    state = context.get("state")
    data = context.get("data", {})

    base = {
        "type": event_type,
        "reference": reference,
        "event_id": evento.get("id"),
        "user_id": evento.get("user_id"),
    }

    nome = reference.get("nome")
    nome_texto = nome if nome else "o item"

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
                    f"O produto {nome_texto} possui apenas "
                    f"{data.get('currentStock')} unidades em estoque."
                ),
            )

        if state == "NEAR_MINIMUM":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.WARNING,
                title="Estoque próximo do mínimo",
                message=(
                    f"O produto {nome_texto} está próximo do limite mínimo "
                    f"de {data.get('minimumStock')} unidades."
                ),
            )

    # ======================
    # IMPORTAÇÃO
    # ======================

    if state == "IMPORT_SUCCESS":
        file_name = data.get("file_name", "arquivo")
        inserted = data.get("inserted", 0)
        rejected = data.get("rejected", 0)

        return NotificationCreate(
            **base,
            severity=NotificationSeverity.SUCCESS,
            title="Importação concluída",
            message=(
                f"Arquivo {file_name} processado. "
                f"{inserted} registros importados e "
                f"{rejected} rejeitados."
            ),
        )

    if state == "IMPORT_PARTIAL":

        file_name = data.get("file_name", "arquivo")
        inserted = data.get("inserted", 0)
        rejected = data.get("rejected", 0)

        return NotificationCreate(
            **base,
            severity=NotificationSeverity.WARNING,
            title="Importação parcialmente concluída",
            message=(
                f"O arquivo {file_name} foi processado com inconsistências. "
                f"{inserted} registros importados e "
                f"{rejected} rejeitados."
            ),
        )

    if state == "IMPORT_ERROR":

        file_name = data.get("file_name", "arquivo")
        rejected = data.get("rejected", 0)

        return NotificationCreate(
            **base,
            severity=NotificationSeverity.CRITICAL,
            title="Falha na importação",
            message=(
                f"A importação do arquivo {file_name} falhou. "
                f"{rejected} registros foram rejeitados."
            ),
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
                message=f"O produto {nome_texto} está vencido há {abs(dias)} dias."
            )

        if state == "NEAR_EXPIRATION":
            return NotificationCreate(
                **base,
                severity=NotificationSeverity.WARNING,
                title="Produto próximo do vencimento",
                message=f"O produto {nome_texto} vencerá em {dias} dias."
            )

    # ======================
    # ERROR
    # ======================
    if event_type == "ERROR":
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
            title="Sugestão de reposição",
            message=(
                f"Pode ser um bom momento para repor o produto {nome_texto}. "
                f"Verifique o painel de estoque."
            )
        )

    return None