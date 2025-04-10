import uuid

from pydantic import BaseModel, Field

from db.Models import CarUpdatesDataModel
from Utils.Internacionalization import ModelsDescriptionTexts


class CarUpdatesModel(BaseModel):
    id_car: uuid.UUID = Field(description=ModelsDescriptionTexts.CAR_ID)
    updates: CarUpdatesDataModel = Field(description=ModelsDescriptionTexts.UPDATES)
