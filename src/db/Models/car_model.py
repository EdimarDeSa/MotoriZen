import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from db.Models.base_model import BaseModelDb, NewBaseModelDb


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


class NewCarModel(BaseModel):
    cd_brand: int = Field(description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: str = Field(max_length=100, description="Model of the car")
    year: int = Field(lt=(datetime.now().year + 1), description="Year of the car")
    color: str = Field(max_length=25, description="Color of the car")
    license_plate: str = Field(max_length=10, description="License plate of the car")
    odometer: Optional[float] = Field(default=0.0, description="Odometer of the car")


class UpdateCarModel(BaseModel):
    cd_brand: int = Field(description="Brand id")
    renavam: Optional[str] = Field(default=None, max_length=11, description="Renavam of the car")
    model: str = Field(max_length=100, description="Model of the car")
    year: int = Field(lt=datetime.now().year, description="Year of the car")
    color: str = Field(max_length=25, description="Color of the car")
    license_plate: str = Field(max_length=10, description="License plate of the car")
    odometer: float = Field(description="Odometer of the car")
