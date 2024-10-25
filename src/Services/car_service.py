import base64
import json
import uuid
from typing import Any

from db.Models import BrandModel, CarModel, CarQueryOptionsModel, CarQueryParamsModel, CarUpdatesModel, NewCarModel
from db.Schemas import BrandSchema, CarSchema
from Enums import RedisDbsEnum
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

    def get_cars(
        self, id_user: str, query_params: CarQueryParamsModel, query_options: CarQueryOptionsModel, count: int
    ) -> list[CarModel]:
        self.logger.debug("Starting get_cars")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Getting cars")
            query_params_dict = query_params.model_dump(exclude_none=True)
            query_options_dict = query_options.model_dump(exclude_none=True)

            hash_data = {**query_params_dict, **query_options_dict, "count": count, "id_user": id_user}
            base64_hash = self._create_hash(hash_data)

            cars_schema = self._get_cached_data(base64_hash)

            if cars_schema is None:
                cars_schema = self._car_repository.select_cars(
                    db_session,
                    id_user,
                    query_params_dict,
                    query_options,
                )

                self._cache_data(base64_hash, cars_schema)

            cars_model = [CarModel.model_validate(car_schema, from_attributes=True) for car_schema in cars_schema]

            return cars_model

        except Exception as e:
            raise e

    def get_cars_count(self, id_user: str, query_params: CarQueryParamsModel) -> int:
        self.logger.debug("Starting get_cars_count")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Getting cars count")

            query_params_dict = query_params.model_dump(exclude_none=True)

            cars_count = self._car_repository.select_cars_count(db_session, id_user, query_params_dict)

            return cars_count

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
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def _get_cached_data(self, base64_hash: str) -> list[CarSchema | BrandSchema] | None:
        self.logger.debug("Starting _get_cached_data")
        cars_schema: Any = self._cache_handler.get_data(RedisDbsEnum.CARS, base64_hash)
        self.logger.debug(f"Cached data: {cars_schema if not cars_schema else 'found'}")
        return cars_schema

    def _cache_data(self, base64_hash: str, cars_schema: list[CarSchema | BrandSchema]) -> None:
        self.logger.debug("Starting _cache_data")
        self._cache_handler.set_data(RedisDbsEnum.CARS, base64_hash, cars_schema, ex=300)
        self.logger.debug("Data cached")

    def _create_hash(self, hash_data: dict[str, Any]) -> str:
        self.logger.debug("Starting _create_hash")

        self.logger.debug("Creating hash")
        base64_hash = base64.b64encode(bytes(json.dumps(hash_data), "utf-8")).decode("utf-8")
        self.logger.debug(f"Hash created: {base64_hash}")
        return base64_hash

    def update_car(self, id_user: str, car_id: str, car_updates: CarUpdatesModel) -> CarModel:
        self.logger.debug("Starting update_car")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Updating car <car_id: {car_id}> of <user: {id_user}>")
            self._car_repository.update_car(db_session, id_user, car_id, car_updates)

            car_schema: CarSchema = self._car_repository.select_car_by_id(db_session, id_user, car_id)

            car_model = CarModel.model_validate(car_schema, from_attributes=True)

            db_session.commit()

            return car_model

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def delete_car(self, id_user: str, car_id: str) -> None:
        self.logger.debug("Starting delete_car")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Deleting car <car_id: {car_id}> of <user: {id_user}>")
            self._car_repository.delete_car(db_session, id_user, car_id)

            db_session.commit()

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def get_brands(self) -> list[BrandModel]:
        self.logger.debug("Starting get_brands")
        db_session = self.create_session(write=False)

        try:
            hash_data = {"get_brands": "all_brands"}
            base64_hash = self._create_hash(hash_data)

            brand_schema_list = self._get_cached_data(base64_hash)

            if brand_schema_list is None:
                self.logger.debug("Geting all brands")
                brand_schema_list = self._car_repository.select_brands(db_session)

                self._cache_data(base64_hash, brand_schema_list)

            return [BrandModel.model_validate(brand_schema, from_attributes=True) for brand_schema in brand_schema_list]

        except Exception as e:
            raise e

        finally:
            db_session.close()

    def get_brand(self, id_brand: int) -> BrandModel:
        self.logger.debug("Starting get_brands")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Geting all brands")
            brand_schema: BrandSchema = self._car_repository.select_brand(db_session, id_brand)

            return BrandModel.model_validate(brand_schema, from_attributes=True)

        except Exception as e:
            raise e

        finally:
            db_session.close()
