#backend\backend\services\import_service.py
from fastapi import HTTPException
from backend.database.schemas import IMPORT_SCHEMAS
from backend.services.parser_service import parse_to_dataframe
from backend.services.validation_service import validate_row
from backend.database.repository import Repository
import pandas as pd
from datetime import date, datetime
from decimal import Decimal


def normalize_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, (datetime, date)):
        return value

    if isinstance(value, str):
        v = value.strip()
        if v.lower() in ("", "nan", "none", "null"):
            return None
        return v

    return value

def parse_date(value, fmt=None):
    if isinstance(value, (date, datetime)):
        return value
    if fmt:
        return datetime.strptime(value, fmt).date()
    return value


def process_import(upload_file, conn, import_type="produtos"):
    if import_type not in IMPORT_SCHEMAS:
        raise HTTPException(status_code=400, detail="Tipo de importação inválido.")

    schema = IMPORT_SCHEMAS[import_type]
    df = parse_to_dataframe(upload_file)

    # Verifica colunas obrigatórias
    required_columns = {
        col for col, rules in schema["columns"].items()
        if rules.get("required", False)
    }

    missing = required_columns - set(df.columns)
    if missing:
        # Permite que "ativo" falte, pois vamos criar automaticamente
        missing = missing - {"ativo"}
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Colunas faltando: {', '.join(missing)}"
            )

    repo = Repository(conn)

    inserted = 0
    rejected = 0
    errors = []

    # PREPARAÇÃO PARA PERFORMANCE
    type_cast = {
        "int": lambda v, fmt=None: int(float(v)),
        "float": lambda v, fmt=None: Decimal(str(v)),
        "date": lambda v, fmt=None: parse_date(v, fmt),
        "str": lambda v, fmt=None: str(v).strip(),
        "bool": lambda v, fmt=None: bool(v),
    }

    columns_rules = schema["columns"]

    rows_to_insert = []
    rows_index_map = []
    db_columns = repo.get_table_columns(schema["table"])
    for col in schema["columns"].keys():
        if col not in db_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Coluna '{col}' não existe na tabela {schema['table']}"
            )

    # LOOP SEM INSERT
    for idx, row in enumerate(df.itertuples(index=False), start=1):
        row_dict = row._asdict()

        row_errors = validate_row(row_dict, schema)
        if row_errors:
            rejected += 1
            errors.append({"row": idx, "errors": row_errors})
            continue

        data = {}

        for col, rules in columns_rules.items():
            # Se a coluna é 'ativo', atribui True automaticamente
            if col == "ativo":
                value = True
            else:
                value = normalize_value(row_dict.get(col))  # evita KeyError

            if value is None:
                data[col] = None
                continue

            cast_func = type_cast.get(rules["type"], type_cast["str"])
            data[col] = cast_func(value, rules.get("format"))

        rows_to_insert.append(data)
        rows_index_map.append(idx)

    # BULK INSERT
    if rows_to_insert:
        result = repo.bulk_insert(schema["table"], rows_to_insert)

        # Sucesso total
        if result["failed"] == []:
            inserted += result["success"]

        # Sucesso parcial
        else:
            inserted += result["success"]

            for fail in result["failed"]:
                rejected += 1
                errors.append({
                    "row": rows_index_map[fail["index"]],
                    "errors": [fail["error"]],
                })

    repo.commit()

    return {
        "inserted": inserted,
        "rejected": rejected,
        "errors": errors,
    }
