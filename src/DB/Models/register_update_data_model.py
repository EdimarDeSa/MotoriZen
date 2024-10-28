import uuid
from datetime import date, time
from typing import Optional, Self

from pydantic import Field, model_validator

from DB.Models.base_model import BaseModelDb
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError


class RegisterUpdateDataModel(BaseModelDb):
    cd_car: Optional[uuid.UUID] = Field(description="Car id")
    distance: Optional[float] = Field(description="Distance traveled")
    working_time: Optional[time] = Field(description="Duration of the trip")
    mean_consuption: Optional[float] = Field(description="Mean consuption of the car")
    number_of_trips: Optional[int] = Field(description="Number of trips")
    total_value: Optional[float] = Field(description="Total value of the trips")
    register_date: Optional[date] = Field(description="Date of the trip")

    @model_validator(mode="after")
    def validate_updates_value(self) -> Self:
        self.model_fields_set
        if all(
            [
                # self.cd_car is None,
                # self.distance is None,
                # self.working_time is None,
                # self.mean_consuption is None,
                # self.number_of_trips is None,
                # self.total_value is None,
                # self.register_date is None,
                getattr(self, field) is None
                for field in self.model_fields_set
            ]
        ):
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_UPDATES_DATA,
                detail="Invalid updates data. Please, provide at least one value to update.",
            )
        return self
