import pandas as pd
from datetime import datetime

def validate_row(row, schema):
    errors = []

    for col, rules in schema["columns"].items():
        val = row.get(col)

        # Trata NaN como None
        if pd.isna(val):
            val = None

        # Campo obrigatório
        if rules["required"] and (val is None or str(val).strip() == ""):
            errors.append(f"{col} vazio")
            continue

        if val is None:
            continue  # campo opcional vazio é OK

        field_type = rules["type"]

        if field_type == "float":
            try:
                float(val)
            except:
                errors.append(f"{col} inválido (esperado número)")

        elif field_type == "int":
            try:
                int(float(val))
            except:
                errors.append(f"{col} inválido (esperado inteiro)")

        elif field_type == "date":
            try:
                if isinstance(val, pd.Timestamp):
                    pass  # já é data válida

                elif isinstance(val, datetime):
                    pass  # já é data válida

                elif isinstance(val, date):
                    pass  # já é data válida

                else:
                    datetime.strptime(str(val).strip(), rules.get("format", "%Y-%m-%d"))

            except Exception:
                errors.append(
                    f"{col} inválido (formato esperado {rules.get('format', '%Y-%m-%d')})"
                )

    # =========================
    # VALIDAÇÕES DE NEGÓCIO
    # =========================
    if schema["table"] == "app_core.movimentacoes_internas":
        errors.extend(validate_movimentacao_interna(row))

    return errors

def validate_movimentacao_interna(row):
    errors = []

    # quantidade
    try:
        qtd = float(row.get("quantidade"))
        if qtd <= 0:
            errors.append("quantidade deve ser maior que zero")
    except:
        errors.append("quantidade inválida")

    # origem != destino
    origem = str(row.get("origem")).strip() if row.get("origem") else None
    destino = str(row.get("destino")).strip() if row.get("destino") else None

    if origem and destino and origem == destino:
        errors.append("origem e destino não podem ser iguais")

    # tipo
    tipo = row.get("tipo")
    if tipo:
        tipo = str(tipo).strip().upper()

    if tipo not in ("CONSUMO", "PRODUCAO"):
        errors.append("tipo de movimentação inválido (esperado CONSUMO ou PRODUCAO)")

    return errors

