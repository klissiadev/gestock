from pydantic import BaseModel
from datetime import date
from typing import Optional

class LogImportacaoCreate(BaseModel):
    nome_arquivo: str
    qntd_registros: int
    status: str
    msg_erro: Optional[str] = None
    id_usuario: int

class LogImportacao(LogImportacaoCreate):
    id_log_importacao: int
    data_importacao: date
