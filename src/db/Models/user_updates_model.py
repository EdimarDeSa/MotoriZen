from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserUpdatesModel(BaseModel):
    first_name: Optional[str] = Field(
        default=None, max_length=50, min_length=3, examples=["Eduardo"], description="User first name"
    )
    last_name: str = Field(
        default=None, max_length=100, min_length=3, examples=["Eduardo"], description="User last name"
    )
    birthdate: Optional[date] = Field(default=None, description="User birthdate", examples=["2000-01-01"])

    @field_validator("birthdate", mode="after")
    @classmethod
    def validate_birthdate(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Birthdate must be in the past.")
        return value
