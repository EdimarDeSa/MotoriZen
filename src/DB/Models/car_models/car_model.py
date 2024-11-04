import uuid
from typing import Optional

from pydantic import Field

from DB.Models.base_model import BaseModelDb


class CarModel(BaseModelDb):
    id_car: uuid.UUID = Field(description="Car id")
    cd_user: uuid.UUID = Field(description="User id")
    cd_brand: int = Field(description="Brand id")
    renavam: Optional[str] = Field(description="Renavam of the car")
    model: str = Field(description="Model of the car")
    year: int = Field(description="Year of the car")
    color: str = Field(description="Color of the car")
    license_plate: str = Field(description="License plate of the car")
    odometer: float = Field(description="Odometer of the car")
    is_active: bool = Field(default=True, description="If the car is active")
