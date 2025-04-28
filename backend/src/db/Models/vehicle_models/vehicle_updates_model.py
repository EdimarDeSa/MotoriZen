import uuid

from pydantic import BaseModel, Field

from db.Models import VehicleUpdatesDataModel
from Utils.Internacionalization import ModelsDescriptionTexts


class VehicleUpdatesModel(BaseModel):
    id_vehicle: uuid.UUID = Field(description=ModelsDescriptionTexts.VEHICLE_ID)
    updates: VehicleUpdatesDataModel = Field(description=ModelsDescriptionTexts.UPDATES)
