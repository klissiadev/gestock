from pydantic import BaseModel
from typing import Optional

class moviment_filters(BaseModel):
    orderBy: str
    isAsc: bool
    search: Optional[str] = None