#transforma arquivos enviados em dataframes
from io import BytesIO
import pandas as pd
from fastapi import HTTPException
from charset_normalizer import from_bytes
import csv

import unicodedata
import re

def read_uploaded_file(upload_file):
    # transforma upload_file do FastAPI em um conteúdo em bytes
    upload_file.file.seek(0) # reseta o ponteiro para o início do arquivo
    content = upload_file.file.read() # ler o conteúdo do arquivo em bytes
    upload_file.file.seek(0) # reseta novamente o ponteiro (boa prática)
    return content # retorna os bytes lidos


def detect_encoding(content: bytes) -> str:
    """Detecta a codificação do arquivo CSV."""
    result = from_bytes(content).best() # detecta a codificação correta
    if not result or not result.encoding:
        # fallback seguro
        return "utf-8" # caso falhe a detecção
    return result.encoding


def parse_to_dataframe(upload_file):
    content = read_uploaded_file(upload_file)
    filename = upload_file.filename.lower()

    def normalize_column(col: str) -> str:
        col = col.strip().lower()
        col = col.replace("\ufeff", "")  # remove BOM
        col = unicodedata.normalize("NFKD", col)
        col = col.encode("ascii", "ignore").decode("ascii")
        col = re.sub(r"\s+", "_", col)
        return col

    # leitura do arquivo e transformação em DataFrame
    try:
        # --------------------------
        # CSV → detecta encoding
        # --------------------------
        if filename.endswith(".csv"):
            encoding = detect_encoding(content)

            # detecta delimitador automaticamente
            sample = content[:1024].decode(encoding, errors="ignore")
            dialect = csv.Sniffer().sniff(sample, delimiters=";,")
            sep = dialect.delimiter

            df = pd.read_csv(BytesIO(content), encoding=encoding, sep=sep)
            # normalização das colunas
            df.columns = [normalize_column(c) for c in df.columns]
            # tenta converter datas comuns no sistema (GG/MM/AAAA) para o formato AAAA-MM-DD
            for col in ["data_cadastro", "data_validade"]:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
                    df[col] = df[col].apply(
                        lambda x: x.strftime("%Y-%m-%d") if pd.notna(x) else None
                    )

        # --------------------------
        # XLSX → não usa encoding
        # --------------------------
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(content), engine="openpyxl")
            df.columns = [normalize_column(c) for c in df.columns]

            for col in ["data_cadastro", "data_validade"]:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                    df[col] = df[col].apply(
                        lambda x: x.strftime("%Y-%m-%d") if pd.notna(x) else None
                    )

        else:
            raise HTTPException(status_code=400, detail="Formato não suportado.")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")
    
    return df
