import uuid

from db.Models import RegisterUpdateDataModel
from pydantic import BaseModel, Field
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterUpdatesModel(BaseModel):
    id_register: uuid.UUID = Field(description=ModelsDescriptionTexts.REGISTER_ID)
    updates: RegisterUpdateDataModel = Field(description=ModelsDescriptionTexts.UPDATES)
