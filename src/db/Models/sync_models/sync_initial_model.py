from datetime import datetime

from pydantic import BaseModel

from db.Models.brand_models.brand_model import BrandModel
from db.Models.car_models.car_model import CarModel
from db.Models.fuel_type_model import FuelTypeModel
from db.Models.register_models.register_model import RegisterModel
from db.Models.user_models.user_model import UserModel


class SyncInitialModel(BaseModel):
    user_data: UserModel
    brands: list[BrandModel]
    fuel_types: list[FuelTypeModel]
    cars: list[CarModel]
    registers: list[RegisterModel]
    last_pulled_at: datetime
