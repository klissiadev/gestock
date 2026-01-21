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
            date_format = rules.get("format", "%Y-%m-%d")
            try:
                datetime.strptime(str(val), date_format)
            except:
                errors.append(f"{col} inválido (formato esperado {date_format})")

    # =========================
    # VALIDAÇÕES DE NEGÓCIO
    # =========================
    if schema["table"] == "app_core.movimentacoes_internas":
        errors.extend(validate_movimentacao_interna(row))

    return errors

def validate_movimentacao_interna(row):
    errors = []

    # quantidade > 0
    qtd = row.get("quantidade")
    if qtd is not None and qtd <= 0:
        errors.append("quantidade deve ser maior que zero")

    # origem ≠ destino
    origem = row.get("origem")
    destino = row.get("destino")
    if origem and destino and origem == destino:
        errors.append("origem e destino não podem ser iguais")

    # tipo válido
    # tipo válido
    tipo = row.get("tipo")
    if tipo not in ("CONSUMO", "PRODUCAO"):
        errors.append("tipo de movimentação inválido (esperado CONSUMO ou PRODUCAO)")


    return errors
