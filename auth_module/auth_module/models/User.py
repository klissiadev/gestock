from enum import Enum
from uuid import UUID
from pydantic import EmailStr, BaseModel, Field, ConfigDict
from typing import Optional

class UserRole(str, Enum):
    ADMIN = "admin"
    GESTOR = "gestor"

# Esquema para o Cadastro 
class UserCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8) # Validação básica de tamanho
    papel: UserRole = Field(..., max_length=6) # Validação para aceitar apenas "admin" ou "gestor"

# Esquema para Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Retorno da API
class UserPublic(BaseModel):
    id: UUID
    nome: str
    papel: UserRole

    model_config = ConfigDict(from_attributes=True)

# Modelo Interno
class UserDB(BaseModel):
    id: Optional[UUID] = None
    nome: str
    email: EmailStr
    senha_hash: bytes
    papel: UserRole = UserRole.GESTOR
    ativo: bool = True
    
    model_config = ConfigDict(from_attributes=True)




