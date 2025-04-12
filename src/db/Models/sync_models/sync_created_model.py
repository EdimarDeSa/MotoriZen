from datetime import datetime

from pydantic import BaseModel

from db.Models.brand_models.brand_model import BrandModel
from db.Models.car_models.car_model import CarModel
from db.Models.fuel_type_model import FuelTypeModel
from db.Models.register_models.register_model import RegisterModel


class SyncCreatedBrandsModel(BaseModel):
    brands: list[BrandModel]
    last_pulled_at: datetime


class SyncCreatedFuelTypesModel(BaseModel):
    fuel_types: list[FuelTypeModel]
    last_pulled_at: datetime


class SyncCreatedCarsModel(BaseModel):
    cars: list[CarModel]
    last_pulled_at: datetime


class SyncCreatedRegistersModel(BaseModel):
    registers: list[RegisterModel]
    last_pulled_at: datetime


class SyncCreatedModel(BaseModel):
    brands: SyncCreatedBrandsModel | None
    fuel_types: SyncCreatedFuelTypesModel | None
    cars: SyncCreatedCarsModel | None
    registers: SyncCreatedRegistersModel | None
