import uuid

from db.Models.car_model import CarModel, NewCarModel, UpdateCarModel
from db.Schemas.car_schema import CarSchema
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Repositories.car_repository import CarRepository
from Utils.redis_handler import RedisHandler

from .base_service import BaseService


class CarService(BaseService):
    def __init__(self) -> None:
        self._car_repository = CarRepository()
        self._cache_handler = RedisHandler()
        self.create_logger(__name__)

    def get_car(self, id_user: str, car_id: str) -> CarModel:
        self.logger.debug("Starting get_car")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug(f"Getting car <car_id: {car_id}> for <user: {id_user}>")

            car_schema: CarSchema = self._car_repository.select_car_by_id(db_session, id_user, car_id)

            car_model = CarModel.model_validate(car_schema, from_attributes=True)

            return car_model

        except Exception as e:
            raise e

    def create_car(self, id_user: uuid.UUID, new_car: NewCarModel) -> None:
        self.logger.debug("Starting create_car")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Creating car for <user: {id_user}>")
            self._car_repository.insert_car(db_session, id_user, new_car)

            db_session.commit()

        except Exception as e:
            self.logger.exception(e)
            db_session.rollback()
            raise e

        finally:
            db_session.close()
