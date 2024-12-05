import uuid
from datetime import date, time

from pydantic import Field

from DB.Models.base_model import BaseModelDb
from Utils.Internacionalization import ModelsDescriptionTexts


class RegisterModel(BaseModelDb):
    id_register: uuid.UUID = Field(description=ModelsDescriptionTexts.REGISTER_ID)
    cd_user: uuid.UUID = Field(description=ModelsDescriptionTexts.USER_CD)
    cd_car: uuid.UUID = Field(description=ModelsDescriptionTexts.CAR_CD)
    distance: float = Field(description=ModelsDescriptionTexts.DISTANCE)
    working_time: time = Field(description=ModelsDescriptionTexts.WORKING_TIME)
    mean_consuption: float = Field(description=ModelsDescriptionTexts.MEAN_CONSUMPTION)
    number_of_trips: int = Field(description=ModelsDescriptionTexts.NUMBER_OF_TRIPS)
    total_value: float = Field(description=ModelsDescriptionTexts.TOTAL_VALUE)
    register_date: date = Field(description=ModelsDescriptionTexts.REGISTER_DATE)
