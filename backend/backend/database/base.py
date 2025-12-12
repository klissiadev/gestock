#conexão com o banco de dados
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5432"),
            dbname=os.getenv("PG_DATABASE", "meubanco"),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "postgres"),
            cursor_factory=RealDictCursor,
            connect_timeout=5
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco: {e}")

def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()