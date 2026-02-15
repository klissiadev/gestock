import os
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
import atexit
from pathlib import Path
from admin_module.utils.env_loader import load_env_from_root

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