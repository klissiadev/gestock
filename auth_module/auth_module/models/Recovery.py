from pydantic import BaseModel, EmailStr, Field

class RecoveryRequest(BaseModel):
    email: EmailStr 

class PasswordResetConfirm(BaseModel):
    token: str = Field(..., description="O token recebido por e-mail")
    new_password: str = Field(..., min_length=8, max_length=12, description="A nova senha do usuário")