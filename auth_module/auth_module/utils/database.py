import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
import atexit
from auth_module.utils.env_loader import load_env_from_root
from pydantic import EmailStr
from auth_module.models.User import UserDB
from uuid import UUID

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

def this_user_exists(email: EmailStr) -> bool:
    """Busca se há usuario com um e-mail especifico.
    Retorna: True ou False 
    """
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM app_core.usuarios WHERE email= %s ", (email, ))
            return cur.fetchone() is not None 

def register_user(user: UserDB):
    """Cadastra o usuario no banco de dados. 
    Retorna nada
    """
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO app_core.usuarios (nome, papel, senha_hash, email) 
                VALUES (%s, %s, %s, %s);
                """,
                (user.nome, user.papel, user.senha_hash, user.email, )
            )
        conn.commit()


def get_user_by_email(email: EmailStr) -> UserDB | None:
    """Busca usuario através de E-mail e retornar como objeto UserDB"""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM app_core.usuarios WHERE email = %s", (email,))
            data = cur.fetchone()
            if data:
                return UserDB.model_validate(data)
            return None
        
def get_user_by_id(id: UUID) -> UserDB | None:
    """Busca usuario através do ID e retornar como objeto UserDB"""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM app_core.usuarios WHERE id = %s", (id,))
            data = cur.fetchone()
            if data:
                return UserDB.model_validate(data)
            return None
        




            