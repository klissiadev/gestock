from pydantic import BaseModel

class product_filters(BaseModel):
    orderBy: str
    isAsc: bool