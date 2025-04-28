import uuid
from typing import Optional

from pydantic import BaseModel, Field

from db.Models.range_model import RangeModel
from Utils.Internacionalization import ModelsDescriptionTexts


class VehicleQueryFiltersModel(BaseModel):
    id_vehicle: Optional[uuid.UUID] = Field(default=None, description=ModelsDescriptionTexts.VEHICLE_CD)
    cd_brand: Optional[int] = Field(default=None, description=ModelsDescriptionTexts.CD_BRAND)
    renavam: Optional[str] = Field(default=None, max_length=11, description=ModelsDescriptionTexts.RENAVAM)
    model: Optional[str] = Field(default=None, max_length=100, description=ModelsDescriptionTexts.VEHICLE_MODEL)
    year: Optional[RangeModel[int]] = Field(default=None, description=ModelsDescriptionTexts.VEHICLE_YEAR)
    color: Optional[str] = Field(default=None, max_length=25, description=ModelsDescriptionTexts.VEHICLE_COLOR)
    license_plate: Optional[str] = Field(default=None, max_length=10, description=ModelsDescriptionTexts.LICENSE_PLATE)
    odometer: Optional[RangeModel[float]] = Field(default=None, description=ModelsDescriptionTexts.ODOMETER)
    is_active: Optional[bool] = Field(default=None, description=ModelsDescriptionTexts.IS_ACTIVE)
