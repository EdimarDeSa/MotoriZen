import uuid

from pydantic import BaseModel, Field

from DB.Models import CarUpdatesDataModel


class CarUpdatesModel(BaseModel):
    id_car: uuid.UUID = Field(description="Car id")
    updates: CarUpdatesDataModel = Field(description="Car updates data")
