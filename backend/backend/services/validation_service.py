import pandas as pd
from datetime import datetime

def validate_row(row, schema):
    errors = []

    for col, rules in schema["columns"].items():
        val = row.get(col)

        # Campo obrigatório
        if rules.get("required") and (pd.isna(val) or str(val).strip() == ""):
            errors.append(f"{col} vazio")
            continue

        # Se campo não é obrigatório e está vazio, ignora
        if pd.isna(val) or str(val).strip() == "":
            continue

        field_type = rules.get("type")

        # ===== validação por tipo =====
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
            date_format = rules.get("format", "%Y-%m-%d")
            try:
                datetime.strptime(str(val), date_format)
            except:
                errors.append(
                    f"{col} inválido (formato esperado: {date_format})"
                )

    return errors