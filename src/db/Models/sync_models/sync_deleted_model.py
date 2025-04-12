from datetime import datetime

from pydantic import BaseModel

from db.Models.brand_models.brand_model import BrandModel
from db.Models.car_models.car_model import CarModel
from db.Models.fuel_type_model import FuelTypeModel
from db.Models.register_models.register_model import RegisterModel
from db.Models.user_models.user_model import UserModel


class SyncDeletedBrandModel(BaseModel):
    brands: list[BrandModel]
    last_pulled_at: datetime


class SyncDeletedFuelTypesModel(BaseModel):
    fuel_types: list[FuelTypeModel]
    last_pulled_at: datetime


class SyncDeletedCarsModel(BaseModel):
    cars: list[CarModel]
    last_pulled_at: datetime


class SyncUpdatesRegistersModel(BaseModel):
    registers: list[RegisterModel]
    last_pulled_at: datetime


class SyncDeletedModel(BaseModel):
    user_data: UserModel
    brands: SyncDeletedBrandModel
    fuel_types: SyncDeletedFuelTypesModel
    cars: SyncDeletedCarsModel
    registers: SyncUpdatesRegistersModel
