from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, HTTPStatus
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from auth_module.models.User import UserCreate
from auth_module.utils.database import this_user_exists


def create_user(user: UserCreate):
    """Registrando usuario
    1. Verificar se e-mail já foi cadastrado dentro do banco de dados
    2. Criptografar senha -> Criar o UserDB
    3. Salvar no Banco de Dados 
    """

    if (this_user_exists(user.email)):
        raise HTTPException(
            status_code=409, 
            detail='Email já está em uso',
        )
    
    # Criptografar senha

    # Montar usuario

    # Salvar no banco de dados

def login():
    # Receber usuario
    # Verificar se email existe 
    # Se sim: verifica senha
    # Tudo certo? Devolve token de acesso
    
    

