from pydantic import BaseModel
from typing import Optional

class transaction_filters(BaseModel):
    orderBy: str
    isAsc: bool
    searchTerm: Optional[str] = None