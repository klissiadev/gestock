#transforma arquivos enviados em dataframes
from io import BytesIO
import pandas as pd
from fastapi import HTTPException

def read_uploaded_file(upload_file):
    upload_file.file.seek(0)
    return upload_file.file.read()

def parse_to_dataframe(upload_file):
    content = read_uploaded_file(upload_file)
    filename = upload_file.filename.lower()

    bio = BytesIO(content)

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(bio)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(bio, engine="openpyxl")
        else:
            raise HTTPException(status_code=400, detail="Formato não suportado.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")

    df.columns = [c.strip().lower() for c in df.columns]

    return df
