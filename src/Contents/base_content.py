from typing import Any

from pydantic import BaseModel, Field

from Utils.Internacionalization.internacionalization_handler import InternationalizationManager
from Utils.Internacionalization.languages_enum import LanguageEnum
from Utils.Internacionalization.messages_enum import MessagesEnum

int_mngr = InternationalizationManager()


class BaseContent(BaseModel):
    rc: int = Field(
        default=0,
        description=int_mngr.get_message(LanguageEnum.PT_BR, MessagesEnum.RESPONSE_CODE),
    )
    data: Any = Field(default=None, description="Return data, if any")
    # errors: list[ErrorModel] | None = Field(default=None, description="Return error, if any")
