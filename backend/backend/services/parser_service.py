"""
Processa o arquivo enviado (CSV/XLSX), valida colunas e valores,
e insere produtos válidos no banco. Retorna quantos foram inseridos,
quantos foram rejeitados e os erros encontrados.
"""

from io import BytesIO
import pandas as pd
from fastapi import HTTPException


REQUIRED_COLUMNS = {"nome", "preco", "quantidade"}


def _read_file_bytes(upload_file):
    upload_file.file.seek(0)
    content = upload_file.file.read()
    return content


def parse_dataframe_from_upload(upload_file):
    content = _read_file_bytes(upload_file)
    filename = upload_file.filename.lower()

    bio = BytesIO(content)

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(bio)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(bio, engine="openpyxl")
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {str(e)}")

    # Normalize column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Checar colunas obrigatórias
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(status_code=400, detail=f"Colunas faltando: {', '.join(missing)}")

    return df


def validate_row(row, index):
    errors = []

    # nome
    nome = row.get("nome")
    if pd.isna(nome) or str(nome).strip() == "":
        errors.append("nome vazio")

    # preco
    preco = row.get("preco")
    try:
        preco_v = float(preco)
        if preco_v < 0:
            errors.append("preco negativo")
    except Exception:
        errors.append("preco inválido")

    # quantidade
    quantidade = row.get("quantidade")
    try:
        quantidade_v = int(float(quantidade))
        if quantidade_v < 0:
            errors.append("quantidade negativa")
    except Exception:
        errors.append("quantidade inválida")

    return errors


def process_and_insert(upload_file, conn):
    df = parse_dataframe_from_upload(upload_file)

    inserted = 0
    rejected = 0
    errors = []

    cursor = conn.cursor()

    for idx, row in df.iterrows():
        row_data = {col: row[col] for col in df.columns}

        # validações
        row_errors = validate_row(row_data, idx + 1)
        if row_errors:
            rejected += 1
            errors.append({"row": idx + 1, "errors": row_errors})
            continue

        # valores convertidos
        try:
            nome = str(row_data["nome"]).strip()
            preco = float(row_data["preco"])
            quantidade = int(float(row_data["quantidade"]))
        except Exception as e:
            rejected += 1
            errors.append({"row": idx + 1, "errors": [f"erro ao processar linha: {str(e)}"]})
            continue

        # INSERT direto no PostgreSQL
        try:
            cursor.execute(
                """
                INSERT INTO produtos (nome, preco, quantidade)
                VALUES (%s, %s, %s)
                """,
                (nome, preco, quantidade)
            )
            inserted += 1

        except Exception as e:
            rejected += 1
            errors.append({"row": idx + 1, "errors": [f"erro ao inserir: {str(e)}"]})

    # commit ou rollback
    try:
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao gravar no banco: {str(e)}")
    finally:
        cursor.close()

    return {
        "inserted": inserted,
        "rejected": rejected,
        "errors": errors
    }
