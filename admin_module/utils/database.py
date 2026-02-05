import os
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv

load_dotenv()

# Inicializamos o Pool Globalmente
db_pool = ConnectionPool(
    conninfo=os.getenv("DATABASE_URL"),
    min_size=2, 
    max_size=15,
    timeout=5.0
)

def get_db_connection():
    """Função utilitária para os módulos pegarem uma conexão"""
    return db_pool.connection()