# Aqui vao ficar as funcoes auxiliares de segurança

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

SECRET_KEY = 'your-secret-key'  
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended() 

# Criador de token com base na informacao: classe Usuario
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




# Funcoes relacionadas a senha
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)
