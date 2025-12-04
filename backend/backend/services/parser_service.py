
"""
Processa o arquivo enviado (CSV/XLSX), valida colunas e valores,
e insere produtos válidos no banco. Retorna quantos foram inseridos,
quantos foram rejeitados e os erros encontrados.
"""

from io import BytesIO
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.product_model import Produto

REQUIRED_COLUMNS = {"nome", "preco", "quantidade"}

def _read_file_bytes(upload_file):
    # Lê tudo em memória (limitado pelo check de tamanho já feito)
    upload_file.file.seek(0)
    content = upload_file.file.read()
    return content

def parse_dataframe_from_upload(upload_file):
    content = _read_file_bytes(upload_file)
    filename = upload_file.filename.lower()

    bio = BytesIO(content)

    try:
        if filename.endswith(".csv"):
            # pd.read_csv aceita BytesIO
            df = pd.read_csv(bio)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(bio, engine="openpyxl")
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {str(e)}")

    # Normalize column names: remove espaços, lower case
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Checar colunas obrigatórias
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(status_code=400, detail=f"Colunas faltando: {', '.join(missing)}")

    return df

def validate_row(row, index):
    errors = []
    # nome não vazio
    nome = row.get("nome")
    if pd.isna(nome) or str(nome).strip() == "":
        errors.append("nome vazio")

    # preco float positivo
    preco = row.get("preco")
    try:
        preco_v = float(preco)
        if preco_v < 0:
            errors.append("preco negativo")
    except Exception:
        errors.append("preco inválido")

    # quantidade integer não-negativa
    quantidade = row.get("quantidade")
    try:
        quantidade_v = int(float(quantidade))
        if quantidade_v < 0:
            errors.append("quantidade negativa")
    except Exception:
        errors.append("quantidade inválida")

    return errors

def process_and_insert(upload_file, db: Session):
    df = parse_dataframe_from_upload(upload_file)

    inserted = 0
    rejected = 0
    errors = []

    # itertuples é mais rápido, mas vamos iterar por index pra reportar linhas
    for idx, row in df.iterrows():
        row_data = {col: row[col] for col in df.columns}
        row_errors = validate_row(row_data, idx + 1)
        if row_errors:
            rejected += 1
            errors.append({"row": idx + 1, "errors": row_errors})
            continue

        # cria objeto
        try:
            produto = Produto(
                nome=str(row_data["nome"]).strip(),
                preco=float(row_data["preco"]),
                quantidade=int(float(row_data["quantidade"]))
            )
            db.add(produto)
            inserted += 1
        except Exception as e:
            rejected += 1
            errors.append({"row": idx + 1, "errors": [f"erro ao inserir: {str(e)}"]})

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao gravar no banco: {str(e)}")

    return {"inserted": inserted, "rejected": rejected, "errors": errors}


