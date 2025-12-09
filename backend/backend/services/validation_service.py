#validação de dados conforme schema
import pandas as pd

def validate_row(row, schema):
    errors = []

    for col, rules in schema["columns"].items():
        val = row.get(col)

        # Campo obrigatório
        if rules["required"] and (pd.isna(val) or str(val).strip() == ""):
            errors.append(f"{col} vazio")
            continue

        # Tipo esperado
        if rules["type"] == "float":
            try:
                float(val)
            except:
                errors.append(f"{col} inválido (esperado número)")
        elif rules["type"] == "int":
            try:
                int(float(val))
            except:
                errors.append(f"{col} inválido (esperado inteiro)")

    return errors
