from typing import Any

from pydantic import BaseModel, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class BaseContent(BaseModel):
    rc: int = Field(
        default=0,
        description=ModelsDescriptionTexts.RESPONSE_CODE,
    )
    data: Any = Field(default=None, description=ModelsDescriptionTexts.BASE_DATA)
    # errors: list[ErrorModel] | None = Field(default=None, description="Return error, if any")
