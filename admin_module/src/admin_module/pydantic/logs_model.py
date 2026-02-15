from pydantic import BaseModel
from datetime import date
from typing import Literal


class MinervaLogsRequest(BaseModel):
    user_name: str | None = None
    period: tuple[date, date] | None = None

class ImportLogsRequest(BaseModel):
    direction: Literal["ASC", "DESC"] = "DESC"
    order_by: str = "registrado_em"
    search_term: str | None = None
    status: str | None = None
    periodo: tuple[date | None, date | None] | None = None
    apenas_erro: bool = False
