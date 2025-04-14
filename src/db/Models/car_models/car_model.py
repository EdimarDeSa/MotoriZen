import uuid
from typing import Optional

from pydantic import Field

from db.Models.base_model import BaseModelDb
from Utils.Internacionalization import ModelsDescriptionTexts


class VehicleModel(BaseModelDb):
    id_vehicle: uuid.UUID = Field(description=ModelsDescriptionTexts.VEHICLE_ID)
    cd_brand: int = Field(description=ModelsDescriptionTexts.CD_BRAND)
    renavam: Optional[str] = Field(description=ModelsDescriptionTexts.RENAVAM)
    model: str = Field(description=ModelsDescriptionTexts.VEHICLE_MODEL)
    year: int = Field(description=ModelsDescriptionTexts.VEHICLE_YEAR)
    color: str = Field(description=ModelsDescriptionTexts.VEHICLE_COLOR)
    cd_fuel_type: int = Field(description=ModelsDescriptionTexts.CD_FUEL_TYPE)
    fuel_capacity: float = Field(description=ModelsDescriptionTexts.FUEL_CAPACITY)
    license_plate: str = Field(description=ModelsDescriptionTexts.LICENSE_PLATE)
    odometer: float = Field(description=ModelsDescriptionTexts.ODOMETER)
    is_active: bool = Field(description=ModelsDescriptionTexts.IS_ACTIVE)
