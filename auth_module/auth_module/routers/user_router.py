import os
from pwdlib import PasswordHash
from auth_module.utils.env_loader import load_env_from_root


# Carregar variaveis de ambiente
load_env_from_root()
teste = os.getenv("DATABASE_URL")

# Hash de senha com o algoritmo recomendado (Argon2)
password_hash = PasswordHash.recommended() 

# Funcoes relacionadas a senha
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

