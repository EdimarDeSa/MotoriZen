import uuid
from datetime import date

from pydantic import EmailStr, Field

from DB.Models.base_model import BaseModelDb
from Utils.Internacionalization import ModelsDescriptionTexts


class UserModel(BaseModelDb):
    id_user: uuid.UUID
    first_name: str = Field(examples=["Eduardo"], description=ModelsDescriptionTexts.FIRST_NAME)
    last_name: str = Field(examples=["Eduardo"], description=ModelsDescriptionTexts.LAST_NAME)
    cd_auth: uuid.UUID = Field(description=ModelsDescriptionTexts.AUTH_CD)
    email: EmailStr = Field(examples=["email@domain.com"], description=ModelsDescriptionTexts.EMAIL)
    birthdate: date = Field(examples=["2000-01-01"], description=ModelsDescriptionTexts.BIRTHDATE)
    is_active: bool = Field(description=ModelsDescriptionTexts.IS_ACTIVE)
