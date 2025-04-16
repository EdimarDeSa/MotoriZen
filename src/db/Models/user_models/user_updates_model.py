from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Utils.Internacionalization import ModelsDescriptionTexts


class UserUpdatesModel(BaseModel):
    first_name: Optional[str] = Field(
        default=None, max_length=50, min_length=3, examples=["Edimar"], description=ModelsDescriptionTexts.FIRST_NAME
    )
    last_name: Optional[str] = Field(
        default=None,
        max_length=100,
        min_length=3,
        examples=["Freitas de Sa"],
        description=ModelsDescriptionTexts.LAST_NAME,
    )
    birthdate: Optional[date] = Field(default=None, description=ModelsDescriptionTexts.BIRTHDATE)

    @field_validator("birthdate", mode="after")
    @classmethod
    def validate_birthdate(cls, value: date) -> date:
        if value >= date.today():
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_UPDATES_DATA, detail="Birthdate must be in the past."
            ).as_http_response()
        return value
