# auth_module/utils/security.py
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Annotated
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from auth_module.models.User import UserPublic
from auth_module.utils.database import get_user_by_email, get_user_by_id
import os
from auth_module.utils.env_loader import load_env_from_root
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

load_env_from_root()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
password_hash = PasswordHash.recommended() 

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def create_access_token(data: dict):
    """Cria o token de login com base em um dicionario"""
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth_scheme)]) -> UserPublic:
    """Verificador de usuario logado. Retorna as informações publicas do usuário"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usr = payload.get("sub")
        if id_usr is None:
            raise credentials_exception
        id_usr_uuid = UUID(id_usr)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_id(id=id_usr_uuid)
    if user is None:
        raise credentials_exception
    
    return UserPublic.model_validate(user)


# Funcoes relacionadas ao tratamento de senhas
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    if isinstance(hashed_password, bytes):
        hashed_password = hashed_password.decode('utf-8')
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> bytes:
    hash_str = password_hash.hash(password)
    return hash_str.encode('utf-8')
