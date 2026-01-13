from pydantic import BaseModel


class LLMRequest(BaseModel):
    question: str