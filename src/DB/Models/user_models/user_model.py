import uuid
from datetime import date

from pydantic import EmailStr, Field

from DB.Models.base_model import BaseModelDb


class UserModel(BaseModelDb):
    id_user: uuid.UUID
    first_name: str = Field(examples=["Eduardo"], description="User first name")
    last_name: str = Field(examples=["Eduardo"], description="User last name")
    cd_auth: uuid.UUID = Field(description="User authentication id")
    email: EmailStr = Field(examples=["email@domain.com"], description="User email")
    birthdate: date = Field(examples=["2000-01-01"], description="User birthdate")
    is_active: bool = Field(description="If the user is active")
