import uuid

from pydantic import BaseModel, Field

from DB.Models import RegisterUpdateDataModel
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterUpdatesModel(BaseModel):
    id_register: uuid.UUID = Field(description=ModelsDescriptionTexts.REGISTER_ID)
    updates: RegisterUpdateDataModel = Field(description=ModelsDescriptionTexts.UPDATES)
