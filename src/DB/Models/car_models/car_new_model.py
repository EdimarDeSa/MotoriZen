from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class CarNewModel(BaseModel):
    cd_brand: int = Field(description=ModelsDescriptionTexts.CD_BRAND)
    renavam: Optional[str] = Field(default=None, max_length=11, description=ModelsDescriptionTexts.RENAVAM)
    model: str = Field(max_length=100, description=ModelsDescriptionTexts.CAR_MODEL)
    year: int = Field(lt=(datetime.now().year + 2), description=ModelsDescriptionTexts.CAR_YEAR)
    color: str = Field(max_length=25, description=ModelsDescriptionTexts.CAR_COLOR)
    license_plate: str = Field(max_length=10, description=ModelsDescriptionTexts.LICENSE_PLATE)
    cd_fuel_type: int = Field(description=ModelsDescriptionTexts.CD_FUEL_TYPE)
    fuel_capacity: int = Field(default=1, gt=1, description=ModelsDescriptionTexts.FUEL_CAPACITY)
    odometer: Optional[float] = Field(default=0.0, description=ModelsDescriptionTexts.ODOMETER)
    is_active: bool = Field(default=True, description=ModelsDescriptionTexts.IS_ACTIVE)
