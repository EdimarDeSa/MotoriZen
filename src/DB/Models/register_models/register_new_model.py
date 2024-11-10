import uuid
from datetime import date, time
from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError


class RegisterNewModel(BaseModel):

    cd_car: uuid.UUID = Field(description="Car id")
    number_of_trips: int = Field(description="Number of trips")
    distance: Optional[float] = Field(
        default=None,
        description="Distance traveled, in kilometers. If odometer is provided, this field will be ignored in user car odometer update.",
    )
    odometer: Optional[float] = Field(
        default=None,
        description="Odometer of the car in kilometers. If distance is provided, this field will be ignored in calculating the distance for reports.",
    )
    working_time: time = Field(description="Duration of the trip")
    mean_consuption: float = Field(description="Mean consuption of the car")
    total_value: float = Field(description="Total value of the trips")
    register_date: date = Field(description="Date of the trip")

    @model_validator(mode="after")
    def validate_distance_and_odometer(self) -> Self:
        if not self.distance and not self.odometer:
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_REGISTER_DATA,
                detail="Please, provide the fields: distance and/or odometer.",
            )

        return self
