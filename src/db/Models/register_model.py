import uuid
from datetime import date, time

from pydantic import Field

from db.Models.base_model import BaseModelDb


class RegisterModel(BaseModelDb):
    id_register: uuid.UUID = Field(description="Register id")
    cd_user: uuid.UUID = Field(description="User id")
    cd_car: uuid.UUID = Field(description="Car id")
    distance: float = Field(description="Distance traveled")
    working_time: time = Field(description="Duration of the trip")
    mean_consuption: float = Field(description="Mean consuption of the car")
    number_of_trips: int = Field(description="Number of trips")
    total_value: float = Field(description="Total value of the trips")
    register_date: date = Field(description="Date of the trip")
