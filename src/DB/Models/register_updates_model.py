import uuid

from pydantic import BaseModel, Field

from DB.Models import RegisterUpdateDataModel


class RegisterUpdatesModel(BaseModel):
    id_register: uuid.UUID = Field(description="Register id")
    updates: RegisterUpdateDataModel = Field(description="Register updates data")
