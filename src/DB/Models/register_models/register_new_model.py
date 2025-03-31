import uuid
from datetime import date, time
from typing import Optional, Self

from pydantic import BaseModel, Field, model_validator

from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterNewModel(BaseModel):

    cd_car: uuid.UUID = Field(description=ModelsDescriptionTexts.CAR_CD)
    number_of_trips: int = Field(description=ModelsDescriptionTexts.NUMBER_OF_TRIPS)
    distance: Optional[float] = Field(
        default=None,
        description=ModelsDescriptionTexts.DISTANCE,
    )
    odometer: Optional[float] = Field(
        default=None,
        description=ModelsDescriptionTexts.ODOMETER,
    )
    working_time: time = Field(description=ModelsDescriptionTexts.WORKING_TIME)
    mean_consuption: float = Field(description=ModelsDescriptionTexts.MEAN_CONSUMPTION)
    total_value: float = Field(description=ModelsDescriptionTexts.TOTAL_VALUE)
    register_date: date = Field(description=ModelsDescriptionTexts.REGISTER_DATE)

    @model_validator(mode="after")
    def validate_distance_and_odometer(self) -> Self:
        if not self.distance and not self.odometer:
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_REGISTER_DATE,
                detail=ModelsDescriptionTexts.INVALID_REGISTER_DATA,
            )

        return self
