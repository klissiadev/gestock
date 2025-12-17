#transforma arquivos enviados em dataframes
from io import BytesIO
import pandas as pd
from fastapi import HTTPException
from charset_normalizer import from_bytes
import csv

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

    # leitura do arquivo e transformação em DataFrame
    try:
        # --------------------------
        # CSV → detecta encoding
        # --------------------------
        if filename.endswith(".csv"):
            encoding = detect_encoding(content)
            
            # Detector de separador
            sample = content[:2048].decode(encoding, errors="ignore")
            try:
                dialect = csv.Sniffer().sniff(sample)
                sep = dialect.delimiter
            except:
                sep = ";"  # fallback comum

            df = pd.read_csv(BytesIO(content), encoding=encoding, sep=sep)

        # --------------------------
        # XLSX → não usa encoding
        # --------------------------
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(content), engine="openpyxl")

        else:
            raise HTTPException(status_code=400, detail="Formato não suportado.")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")

    # Normaliza colunas
    df.columns = [c.strip().lower() for c in df.columns]

    return df
