import os
from psycopg_pool import ConnectionPool
from psycopg import sql
from psycopg.rows import dict_row
import atexit
from env_loader import load_env_from_root

from pydantic import EmailStr


load_env_from_root()

# Inicializamos o Pool Globalmente
db_pool = ConnectionPool(
    conninfo=os.getenv("DATABASE_URL"),
    min_size=0, 
    max_size=15,
    timeout=5.0
)

atexit.register(db_pool.close)

def get_db_connection(timeout=None):
    """Função utilitária para os módulos pegarem uma conexão"""
    return db_pool.connection(timeout=timeout)

def fetch_all_users():
    """Busca os usuarios dentro do banco de dados.
    Retorna: dicionario com eles """
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            data = cur.execute("SELECT * FROM app_core.usuarios").fetchall()
            return data

def verify_user(email: EmailStr) -> bool:
    """Busca se há usuario com um e-mail especifico.
    Retorna: True ou False 
    """
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            data = cur.execute("SELECT * FROM app_core.usuarios WHERE email= %s ", (email, )).fetchall()
            if data:
                print('achou')
            else:
                print('nao achou')        


            