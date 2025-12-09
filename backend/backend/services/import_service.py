from fastapi import HTTPException
from backend.database.schemas import IMPORT_SCHEMAS
from backend.services.parser_service import parse_to_dataframe
from backend.services.validation_service import validate_row
from backend.database.repository import Repository

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

    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        row_errors = validate_row(row_dict, schema)

        if row_errors:
            rejected += 1
            errors.append({"row": idx+1, "errors": row_errors})
            continue

        # Normalização
        data = {}
        for col, rules in schema["columns"].items():
            if rules["type"] == "int":
                data[col] = int(float(row_dict[col]))
            elif rules["type"] == "float":
                data[col] = float(row_dict[col])
            else:
                data[col] = str(row_dict[col]).strip()

        success = repo.insert(schema["table"], data)

        if success is True:
            inserted += 1
        else:
            rejected += 1
            errors.append({"row": idx+1, "errors": [success[1]]})

    repo.commit()
    repo.close()

    return {
        "inserted": inserted,
        "rejected": rejected,
        "errors": errors
    }
