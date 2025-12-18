
from fastapi import HTTPException
from backend.database.schemas import IMPORT_SCHEMAS
from backend.services.parser_service import parse_to_dataframe
from backend.services.validation_service import validate_row
from backend.database.repository import Repository
import pandas as pd
from datetime import date, datetime

def normalize_value(value):
    # Pandas NaN / NaT
    if pd.isna(value):
        return None

    # datetime ou date
    if isinstance(value, (datetime, date)):
        return value

    # Strings problemáticas
    if isinstance(value, str):
        v = value.strip()
        if v.lower() in ("", "nan", "none", "null"):
            return None
        return v

    return value

def process_import(upload_file, conn, import_type="produtos"):
    if import_type not in IMPORT_SCHEMAS:
        raise HTTPException(status_code=400, detail="Tipo de importação inválido.")

    schema = IMPORT_SCHEMAS[import_type]
    df = parse_to_dataframe(upload_file)

    # Verifica colunas
    missing = set(schema["columns"].keys()) - set(df.columns)
    if missing:
        raise HTTPException(status_code=400, detail=f"Colunas faltando: {', '.join(missing)}")

    repo = Repository(conn)
    inserted = 0
    rejected = 0
    errors = []

    

    # Esse For é demoniaco, ele ta sendo culpado pela demora
    # Numa planilha de 3 mil linhas, ele demora 6 minutos
    # É preciso otimizar isso aqui pra melhorar a performance
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        row_errors = validate_row(row_dict, schema)

        if row_errors:
            rejected += 1
            errors.append({"row": idx+1, "errors": row_errors})
            continue

        data = {}

        for col, rules in columns_schema.items():
            raw_value = row_dict.get(col)
            value = normalize_value(raw_value)
            
            # Quantas vezes ele passa aqui? 
            # Resposta: MUITAS VEZES, tipo 23999 vezes
            # print(f"comecou a analisar os valores: {count}")
            # count += 1

            if value is None:
                data[col] = None
                continue

            if rules["type"] == "int":
                data[col] = int(float(value))

            elif rules["type"] == "float":
                data[col] = float(value)

            elif rules["type"] == "date":
                # psycopg2 aceita date ou string YYYY-MM-DD
                data[col] = value

            else:
                data[col] = str(value).strip()

        success = repo.insert(schema["table"], data)

        if success is True:
            inserted += 1
        else:
            rejected += 1
            errors.append({"row": idx+1, "errors": [success[1]]})

    print("depois do for")
    repo.commit()
    repo.close()

    return {
        "inserted": inserted,
        "rejected": rejected,
        "errors": errors
    }
