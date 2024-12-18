import uuid
from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from DB.Models.range_model import RangeModel
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterQueryFiltersModel(BaseModel):
    id_register: Optional[uuid.UUID] = Field(default=None, description=ModelsDescriptionTexts.REGISTER_ID)
    cd_car: Optional[uuid.UUID] = Field(default=None, description=ModelsDescriptionTexts.CAR_CD)
    distance: Optional[RangeModel[float]] = Field(default=None, description=ModelsDescriptionTexts.DISTANCE)
    working_time: Optional[RangeModel[time]] = Field(default=None, description=ModelsDescriptionTexts.WORKING_TIME)
    mean_consuption: Optional[RangeModel[float]] = Field(
        default=None, description=ModelsDescriptionTexts.MEAN_CONSUMPTION
    )
    number_of_trips: Optional[RangeModel[int]] = Field(default=None, description=ModelsDescriptionTexts.NUMBER_OF_TRIPS)
    total_value: Optional[RangeModel[float]] = Field(default=None, description=ModelsDescriptionTexts.TOTAL_VALUE)
    register_date: Optional[RangeModel[date]] = Field(default=None, description=ModelsDescriptionTexts.REGISTER_DATE)
