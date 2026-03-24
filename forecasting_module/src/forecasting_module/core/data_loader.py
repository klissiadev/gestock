import pandas as pd
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def load_anomaly_data(data_corte):
    STRING_CONEXAO = os.getenv("DATABASE_URL")

    if STRING_CONEXAO is None:
        raise ValueError("DATABASE_URL não encontrada no .env")

    query = """
        SELECT *
        FROM app_core.vw_anomaly_input
        WHERE date >= %s
        ORDER BY date ASC;
    """

    with psycopg.connect(STRING_CONEXAO) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (data_corte,))
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)

    # Garantir datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remover datas inválidas
    df = df.dropna(subset=["date"])

    # Criar feature usada no treino
    df["day_of_week"] = df["date"].dt.dayofweek

    # Garantir tipos numéricos
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["sell_price"] = pd.to_numeric(df["sell_price"], errors="coerce")

    # Remover possíveis NaN
    df = df.dropna(subset=["value", "sell_price"])
    
    return df