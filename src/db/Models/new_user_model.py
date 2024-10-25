from datetime import date

from pydantic import EmailStr, Field, field_validator

from db.Models.base_model import NewBaseModelDb


class NewUserModel(NewBaseModelDb):
    first_name: str = Field(max_length=50, min_length=3, examples=["Eduardo"], description="User first name")
    last_name: str = Field(max_length=100, min_length=3, examples=["Eduardo"], description="User last name")
    email: EmailStr = Field(max_length=255, min_length=3, examples=["email@domain.com"], description="User email")
    password: str = Field(examples=["P@s5W0rd"], description="User password")
    birthdate: date

    @field_validator("birthdate", mode="after")
    @classmethod
    def validate_birthdate(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Birthdate cannot be in the future")
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
            raise ValueError("; ".join(errors))

        return value
