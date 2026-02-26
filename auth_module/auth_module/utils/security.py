# auth_module/utils/security.py
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Annotated
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from auth_module.models.User import UserPublic, UserDB
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

# Para o recovery
def create_password_reset_token(user: UserDB):
    """
    Função para criar o token de recuperação. Usa o hash da senha atual como base do segredo.
    Se a senha mudou, o token é invalido
    """
    dynamic_secret = SECRET_KEY + str(user.senha_hash)
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(user.id)}
    return jwt.encode(to_encode, dynamic_secret, algorithm=ALGORITHM)

import jwt # PyJWT
from datetime import datetime, timedelta, timezone

# No seu security.py
def verify_reset_token(token: str):
    try:
        # 1. Decodificamos SEM validar a assinatura apenas para pegar o 'sub' (user_id)
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        user_id = unverified_payload.get("sub")
        
        if not user_id:
            return None

        user = get_user_by_id(user_id)
        if not user:
            return None

        dynamic_secret = SECRET_KEY + str(user.senha_hash)
        payload = jwt.decode(token, dynamic_secret, algorithms=[ALGORITHM])
        return payload.get("sub")

    except jwt.ExpiredSignatureError:
        print("Token expirou!")
        return None
    except (jwt.InvalidTokenError, Exception) as e:
        print(f"Token inválido: {e}")
        return None

def _role_checker(current_user: UserPublic = Depends(get_current_user), allowed_roles: list[str] = ["admin", "gestor"]):
    if current_user.papel not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este recurso."
        )
    return current_user

def require_role(allowed_roles: list[str]):
    """ 
    Dependencia para verificar se o usuário tem um dos papeis permitidos.
    Exemplo de uso: 
    @app.get("/admin-only", dependencies=[Depends(require_role(["admin"]))]) OU
    @app.get("/admin-gestor", dependencies=[Depends(require_role(["admin", "gestor"]))])
    @app.get("/gestor-only", dependencies=[Depends(require_role(["gestor"]))])
    
    retorna HTTP 403 ou Usuario logado
    """
    def role_checker(current_user: UserPublic = Depends(get_current_user)):
        if current_user.papel not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso."
            )
        return current_user
    
    return role_checker

