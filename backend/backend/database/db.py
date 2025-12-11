from psycopg2 import pool
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Cria um pool simples (ajuste minconn/maxconn)
pg_pool = None

def init_db_pool():
    global pg_pool
    if pg_pool is None:
        # parse DATABASE_URL para passar params ao pool (opcional)
        uri = urlparse(DATABASE_URL)
        pg_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            user=uri.username,
            password=uri.password,
            host=uri.hostname,
            port=uri.port or 5432,
            database=uri.path[1:]  # remove leading '/'
        )
    return pg_pool

def get_conn():
    if pg_pool is None:
        init_db_pool()
    return pg_pool.getconn()

def put_conn(conn):
    if pg_pool:
        pg_pool.putconn(conn)
