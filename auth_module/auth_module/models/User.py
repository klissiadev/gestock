from enum import Enum
from pydantic import EmailStr, BaseModel, Field, ConfigDict

class UserRole(str, Enum):
    ADMIN = "admin"
    GESTOR = "gestor"

# Esquema para o Cadastro 
class UserCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8) # Validação básica de tamanho
    papel: UserRole = UserRole.GESTOR

# Esquema para Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Retorno da API
class UserPublic(BaseModel):
    id: int 
    nome: str
    email: EmailStr 
    papel: UserRole
    ativo: bool
    
    model_config = ConfigDict(from_attributes=True)

# Modelo Interno
class UserDB(BaseModel):
    id: int
    nome: str
    email: EmailStr
    senha_hash: str 
    papel: UserRole
    ativo: bool
    
    model_config = ConfigDict(from_attributes=True)




