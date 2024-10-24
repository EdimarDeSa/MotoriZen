from pydantic import BaseModel


class ErrorModel(BaseModel):
    error: str
    description: str
