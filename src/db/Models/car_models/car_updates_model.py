import uuid

from pydantic import BaseModel, Field

from db.Models import CarUpdatesDataModel
from Utils.Internacionalization import ModelsDescriptionTexts


class CarUpdatesModel(BaseModel):
    id_vehicle: uuid.UUID = Field(description=ModelsDescriptionTexts.VEHICLE_ID)
    updates: CarUpdatesDataModel = Field(description=ModelsDescriptionTexts.UPDATES)
