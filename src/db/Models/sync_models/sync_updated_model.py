from datetime import datetime

from pydantic import BaseModel

from db.Models.brand_models.brand_model import BrandModel
from db.Models.car_models.car_model import CarModel
from db.Models.fuel_type_model import FuelTypeModel
from db.Models.register_models.register_model import RegisterModel
from db.Models.user_models.user_model import UserModel


class SyncUpdatedBrandModel(BaseModel):
    brands: list[BrandModel]
    last_pulled_at: datetime


class SyncUpdatedFuelTypesModel(BaseModel):
    fuel_types: list[FuelTypeModel]
    last_pulled_at: datetime


class SyncUpdatedCarsModel(BaseModel):
    cars: list[CarModel]
    last_pulled_at: datetime


class SyncUpdatesRegistersModel(BaseModel):
    registers: list[RegisterModel]
    last_pulled_at: datetime


class SyncUpdatedModel(BaseModel):
    user_data: UserModel
    brands: SyncUpdatedBrandModel
    fuel_types: SyncUpdatedFuelTypesModel
    cars: SyncUpdatedCarsModel
    registers: SyncUpdatesRegistersModel
