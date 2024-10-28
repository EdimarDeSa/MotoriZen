from typing import Any

from pydantic import BaseModel, Field

# from ErrorHandler import ErrorModel


class BaseContent(BaseModel):
    rc: int = Field(default=0, description="Return code, 0 means success")
    data: Any = Field(default=None, description="Return data, if any")
    # errors: list[ErrorModel] | None = Field(default=None, description="Return error, if any")
