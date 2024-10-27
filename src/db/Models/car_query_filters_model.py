import uuid
from typing import Optional

from pydantic import BaseModel, Field


class CarQueryFiltersModel(BaseModel):
    id_car: Optional[uuid.UUID] = Field(default=None, description="Car id")
    cd_brand: Optional[int] = Field(default=None, description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: Optional[str] = Field(default=None, max_length=100, description="Model of the car")
    year: Optional[int] = Field(default=None, description="Year of the car")
    color: Optional[str] = Field(default=None, max_length=25, description="Color of the car")
    license_plate: Optional[str] = Field(default=None, max_length=10, description="License plate of the car")
    odometer: Optional[float] = Field(default=None, description="Odometer of the car")
    is_active: Optional[bool] = Field(default=None, description="If the car is active")
