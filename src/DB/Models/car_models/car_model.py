import uuid
from typing import Optional

from pydantic import Field

from DB.Models.base_model import BaseModelDb
from Utils.Internacionalization import ModelsDescriptionTexts


class CarModel(BaseModelDb):
    id_car: uuid.UUID = Field(description=ModelsDescriptionTexts.CAR_ID)
    cd_user: uuid.UUID = Field(description=ModelsDescriptionTexts.USER_CD)
    cd_brand: int = Field(description=ModelsDescriptionTexts.CD_BRAND)
    renavam: Optional[str] = Field(description=ModelsDescriptionTexts.RENAVAM)
    model: str = Field(description=ModelsDescriptionTexts.CAR_MODEL)
    year: int = Field(description=ModelsDescriptionTexts.CAR_YEAR)
    color: str = Field(description=ModelsDescriptionTexts.CAR_COLOR)
    cd_fuel_type: int = Field(description=ModelsDescriptionTexts.CD_FUEL_TYPE)
    fuel_capacity: float = Field(description=ModelsDescriptionTexts.FUEL_CAPACITY)
    license_plate: str = Field(description=ModelsDescriptionTexts.LICENSE_PLATE)
    odometer: float = Field(description=ModelsDescriptionTexts.ODOMETER)
    is_active: bool = Field(description=ModelsDescriptionTexts.IS_ACTIVE)
