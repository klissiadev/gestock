from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogImportacaoBase(BaseModel):
    arquivo: str
    status: str
    mensagem: Optional[str] = None

class LogImportacaoCreate(LogImportacaoBase):
    pass

class LogImportacao(LogImportacaoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
