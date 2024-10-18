import uuid
from datetime import date, time

from pydantic import Field

from db.Models.base_model import BaseModelDb, NewBaseModelDb


class DayResultModel(BaseModelDb):
    id_day_result: uuid.UUID = Field(serialization_alias="idDayResult")
    cd_user: uuid.UUID = Field(serialization_alias="cdUser", description="User id")
    cd_car: uuid.UUID = Field(serialization_alias="cdCar", description="Car id")
    distance: float = Field(description="Distance traveled")
    duration: time = Field(description="Duration of the trip")
    mean_consuption: float = Field(serialization_alias="meanConsuption", description="Mean consuption of the car")
    number_of_trips: int = Field(serialization_alias="numberOfTrips", description="Number of trips")
    total_value: float = Field(serialization_alias="totalValue", description="Total value of the trips")
    register_date: date = Field(serialization_alias="registerDate", description="Date of the trip")


class NewDayResultModel(NewBaseModelDb):
    cd_user: uuid.UUID = Field(serialization_alias="cdUser", description="User id")
    cd_car: uuid.UUID = Field(serialization_alias="cdCar", description="Car id")
    distance: float = Field(description="Distance traveled")
    duration: time = Field(description="Duration of the trip")
    mean_consuption: float = Field(serialization_alias="meanConsuption", description="Mean consuption of the car")
    number_of_trips: int = Field(default=1, serialization_alias="numberOfTrips", description="Number of trips")
    total_value: float = Field(serialization_alias="totalValue", description="Total value of the trips")
    register_date: date = Field(serialization_alias="registerDate", description="Date of the trip")
