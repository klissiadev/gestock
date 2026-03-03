from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from pydantic import EmailStr, BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class RequestPriority(str, Enum):
    BAIXA = 'BAIXA'
    MEDIA = 'MEDIA'
    ALTA = 'ALTA'

class RequestItem(BaseModel):
    produto_id: int
    quantidade: int
    observacao: Optional[str] = None

class RequestModel(BaseModel):
    titulo: str
    descricao: str
    motivo: str
    prioridade: RequestPriority = RequestPriority.MEDIA
    itens: List[RequestItem]
    created_at: datetime = Field(default_factory=datetime.now)
    
