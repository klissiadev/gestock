from pydantic import BaseModel
from typing import Optional

class transaction_filters(BaseModel):
    orderBy: str
    isAsc: bool
    search: Optional[str] = None