from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CarNewModel(BaseModel):
    cd_brand: int = Field(description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: str = Field(max_length=100, description="Model of the car")
    year: int = Field(lt=(datetime.now().year + 1), description="Year of the car")
    color: str = Field(max_length=25, description="Color of the car")
    license_plate: str = Field(max_length=10, description="License plate of the car")
    odometer: Optional[float] = Field(default=0.0, description="Odometer of the car")
    is_active: bool = Field(default=True, description="If the car is active")
