import uuid

from pydantic import Field

from db.Models.base_model import BaseModelDb, NewBaseModelDb


class DayResultModel(BaseModelDb):
    id_car: uuid.UUID = Field(serialization_alias="idCar")
    cd_user: uuid.UUID = Field(serialization_alias="cdUser", description="User id")
    odometer: float = Field(description="Odometer of the car")


class NewDayResultModel(NewBaseModelDb):
    cd_user: uuid.UUID = Field(serialization_alias="cdUser", description="User id")
    odometer: float = Field(description="Odometer of the car")
