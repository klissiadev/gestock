from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class LogImportacaoBase(BaseModel):
    nome_arquivo: str
    qntd_registros: int
    data_importacao: date  # ou datetime, dependendo da necessidade
    status: str
    msg_erro: Optional[str] = None
    id_usuario: int

class LogImportacaoCreate(LogImportacaoBase):
    pass

class LogImportacaoUpdate(BaseModel):
    nome_arquivo: Optional[str] = None
    qntd_registros: Optional[int] = None
    data_importacao: Optional[date] = None
    status: Optional[str] = None
    msg_erro: Optional[str] = None
    id_usuario: Optional[int] = None

class LogImportacaoOut(LogImportacaoBase):
    id_log_importacao: int