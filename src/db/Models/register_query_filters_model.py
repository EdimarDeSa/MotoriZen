import uuid
from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from db.Models import RangeModel


class RegisterQueryFiltersModel(BaseModel):
    id_register: Optional[uuid.UUID] = Field(default=None, description="Register id")
    cd_car: Optional[uuid.UUID] = Field(default=None, description="Car id")
    distance: Optional[RangeModel[float]] = Field(default=None, description="Distance traveled")
    working_time: Optional[RangeModel[time]] = Field(default=None, description="Initial duration of the trip.")
    mean_consuption: Optional[RangeModel[float]] = Field(default=None, description="Mean consuption of the car")
    number_of_trips: Optional[RangeModel[int]] = Field(default=None, description="Number of trips")
    total_value: Optional[RangeModel[float]] = Field(default=None, description="Total value of the trips")
    register_date: Optional[RangeModel[date]] = Field(default=None, description="Date of the trip")
