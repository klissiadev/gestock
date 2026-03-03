import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from typing import Literal
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


def this_user_exists(email: EmailStr) -> Literal["ativo", "inativo", "nao_existe"]:
    """
    Busca o status de um usuário pelo e-mail.
    Retorna: 'ativo', 'inativo' ou 'nao_existe'.
    """
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT ativo FROM app_core.usuarios WHERE email = %s", (email,))
            resultado = cur.fetchone()
            
            if resultado is None:
                return "nao_existe"
            
            if resultado["ativo"] is True:
                return "ativo"
            
            return "inativo"

def register_user(user: UserDB, check: str):
    """Cadastra o usuario no banco de dados. 
    Retorna nada
    """
    match check:
        case "nao_existe":
            query = """
            INSERT INTO app_core.usuarios (nome, papel, senha_hash, email) 
            VALUES (%s, %s, %s, %s);
            """
        case "inativo":
            query = """
            UPDATE app_core.usuarios
            SET nome = %s, papel = %s, senha_hash = %s, ativo = true, created_at = NOW()
            WHERE email = %s;   
            """

    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, (user.nome, user.papel, user.senha_hash, user.email))
        conn.commit()

def delete_user(user_id: UUID):
    """Apaga (soft delete) usuario do banco de dados"""
    with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE app_core.usuarios SET ativo = false WHERE id = %s", (user_id,))
                linhas_afetadas = cur.rowcount
            conn.commit()
    return linhas_afetadas > 0

def get_user_by_email(email: EmailStr) -> UserDB | None:
    """Busca usuario através de E-mail e retornar como objeto UserDB"""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM app_core.usuarios WHERE email = %s AND ativo = %s", (email, True, ))
            data = cur.fetchone()
            if data:
                return UserDB.model_validate(data)
            return None
        
def get_user_by_id(id: UUID) -> UserDB | None:
    """Busca usuario através do ID e retornar como objeto UserDB"""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM app_core.usuarios WHERE id = %s AND ativo = %s", (id, True))
            data = cur.fetchone()
            if data:
                return UserDB.model_validate(data)
            return None
        
def change_user_password(id: UUID, senha: bytes) -> bool:
    """Busca usuario através do ID e retornar como objeto UserDB"""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "UPDATE app_core.usuarios SET senha_hash = %s WHERE id = %s", 
                (senha, id,)
            )
        conn.commit()
        return True 
    


        




            