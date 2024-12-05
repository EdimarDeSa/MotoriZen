from datetime import date

from pydantic import EmailStr, Field, field_validator

from DB.Models.base_model import NewBaseModelDb
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Utils.Internacionalization import ModelsDescriptionTexts


class UserNewModel(NewBaseModelDb):
    first_name: str = Field(
        max_length=50, min_length=3, examples=["Eduardo"], description=ModelsDescriptionTexts.FIRST_NAME
    )
    last_name: str = Field(
        max_length=100, min_length=3, examples=["Eduardo"], description=ModelsDescriptionTexts.LAST_NAME
    )
    email: EmailStr = Field(
        max_length=255, min_length=3, examples=["email@domain.com"], description=ModelsDescriptionTexts.EMAIL
    )
    password: str = Field(examples=["P@s5W0rd"], description=ModelsDescriptionTexts.PASSWORD)
    birthdate: date = Field(examples=["09-04-1995"], description=ModelsDescriptionTexts.BIRTHDATE)

    @field_validator("birthdate", mode="after")
    @classmethod
    def validate_birthdate(cls, value: date) -> date:
        if value >= date.today():
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_REGISTER_DATA, detail="Birthdate cannot be in the future"
            ).as_http_response()
        return value

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: str) -> str:
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long")

        if len(value) > 100:
            errors.append("Password must be at most 100 characters long")

        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit")

        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in value):
            errors.append("Password must contain at least one lowercase letter")

        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in value):
            errors.append("Password must contain at least one special character")

        if errors:
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_REGISTER_DATA, detail="; \n".join(errors)
            ).as_http_response()

        return value
