from sqlalchemy import Select
from sqlalchemy.orm import Session, scoped_session

from db.Models.car_models.car_query_filters_model import CarQueryFiltersModel
from db.Models.car_models.car_query_options import CarQueryOptionsModel
from db.Models.register_models.register_query_filters_model import RegisterQueryFiltersModel
from db.Models.register_models.register_query_options import RegisterQueryOptionsModel
from db.Models.user_models.user_model import UserModel
from db.Querys.brand_query_manager import BrandQueryManager
from db.Querys.car_query_manager import CarQueryManager
from db.Querys.fuel_type_query_manager import FuelTypeQueryManager
from db.Querys.user_query_manager import UserQueryManager
from db.Schemas.brand_schema import BrandSchema
from db.Schemas.car_schema import CarSchema
from db.Schemas.fuel_type_schema import FuelTypeSchema
from db.Schemas.register_schema import RegisterSchema
from db.Schemas.user_schema import UserSchema
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Repositories.base_repository import BaseRepository


class SyncRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self._user_querys = UserQueryManager()
        self._brand_querys = BrandQueryManager()
        self._fuel_type_querys = FuelTypeQueryManager()
        self._car_querys = CarQueryManager()
