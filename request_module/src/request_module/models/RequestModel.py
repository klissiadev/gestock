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

class RequestItem(BaseModel):
    produto_id: int
    quantidade: int
    prioridade: bool

class RequestModel(BaseModel):
    titulo: str
    observacao: str
    itens: List[RequestItem]

    
