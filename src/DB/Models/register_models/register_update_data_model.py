import uuid
from datetime import date, time
from typing import Optional, Self

from pydantic import Field, model_validator

from DB.Models.base_model import BaseModelDb
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterUpdateDataModel(BaseModelDb):
    cd_car: Optional[uuid.UUID] = Field(description=ModelsDescriptionTexts.CAR_CD)
    distance: Optional[float] = Field(description=ModelsDescriptionTexts.DISTANCE)
    working_time: Optional[time] = Field(description=ModelsDescriptionTexts.WORKING_TIME)
    mean_consuption: Optional[float] = Field(description=ModelsDescriptionTexts.MEAN_CONSUMPTION)
    number_of_trips: Optional[int] = Field(description=ModelsDescriptionTexts.NUMBER_OF_TRIPS)
    total_value: Optional[float] = Field(description=ModelsDescriptionTexts.TOTAL_VALUE)
    register_date: Optional[date] = Field(description=ModelsDescriptionTexts.REGISTER_DATE)

    @model_validator(mode="after")
    def validate_updates_value(self) -> Self:
        self.model_fields_set
        if all([getattr(self, field) is None for field in self.model_fields_set]):
            raise MotoriZenError(
                err=MotoriZenErrorEnum.INVALID_UPDATES_DATA,
                detail="Invalid updates data. Please, provide at least one value to update.",
            )
        return self
