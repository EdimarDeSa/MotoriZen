from datetime import UTC, datetime

from db.Models.brand_models.brand_model import BrandModel
from db.Models.car_models.car_model import CarModel
from db.Models.car_models.car_query_filters_model import CarQueryFiltersModel
from db.Models.car_models.car_query_options import CarQueryOptionsModel
from db.Models.fuel_type_model import FuelTypeModel
from db.Models.register_models.register_model import RegisterModel
from db.Models.register_models.register_query_filters_model import RegisterQueryFiltersModel
from db.Models.register_models.register_query_options import RegisterQueryOptionsModel
from db.Models.sync_models.sync_initial_model import SyncInitialModel
from db.Models.user_models.user_model import UserModel
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from Enums.redis_dbs_enum import RedisDbsEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Repositories.brand_repository import BrandRepository
from Repositories.car_repository import CarRepository
from Repositories.fuel_type_repository import FuelTypeRepository
from Repositories.register_repository import RegisterRepository
from Repositories.sync_repository import SyncRepository
from Repositories.user_repository import UserRepository
from Services.base_service import BaseService
from Utils.redis_handler import RedisHandler


# TODO: Finalizar implementação
class SyncService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self._sync_repository = SyncRepository()
        self._user_repository = UserRepository()
        self._brand_repository = BrandRepository()
        self._fuel_type_repository = FuelTypeRepository()
        self._car_repository = CarRepository()
        self._register_repository = RegisterRepository()
        self._cache_handler = RedisHandler()
        self.create_logger(__name__)

    def sync_initial(self, id_user: str) -> SyncInitialModel:
        self.logger.debug("Starting sync_initial")
        db_session = self.create_session(write=False)

        try:
            hash_data = {"id_user": id_user, "sync_initial": "sync_initial"}
            hash_key = self.create_hash_key(hash_data)

            sync_data = self.get_user_cached_data(RedisDbsEnum.SYNC_INITIAL, id_user, hash_key)

            if sync_data is None:

                car_qf = CarQueryFiltersModel()
                car_qo = CarQueryOptionsModel(per_page=1000)

                reg_qf = RegisterQueryFiltersModel()
                reg_qo = RegisterQueryOptionsModel(per_page=1000)

                sync_data = {
                    "user_data": self._user_repository.select_user_by_id(db_session, id_user),
                    "brands": self._brand_repository.select_brands(db_session),
                    "fuel_types": self._fuel_type_repository.select_fuel_types(db_session),
                    "cars": self._car_repository.select_cars(db_session, id_user, car_qf, car_qo),
                    "registers": self._register_repository.select_registers(db_session, id_user, reg_qf, reg_qo),
                    "last_pulled_at": datetime.now(UTC),
                }

                self.insert_user_cache_data(RedisDbsEnum.SYNC_INITIAL, id_user, hash_key, sync_data)

            return SyncInitialModel.model_validate(sync_data, from_attributes=True)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=repr(e), headers=None)

            raise e

        finally:
            db_session.close()

    def sync_last_pulled_at(self, id_user: str, last_pulled_at: str) -> None:
        pass

    def sync_updates(self, id_user: str) -> None:
        pass
