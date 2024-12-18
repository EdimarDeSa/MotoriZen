import uuid

from DB.Models import (
    CarModel,
    CarNewModel,
    CarQueryFiltersModel,
    CarQueryOptionsModel,
    CarQueryResponseModel,
    CarUpdatesDataModel,
)
from DB.Schemas import CarSchema
from Enums import RedisDbsEnum
from Repositories.car_repository import CarRepository
from Utils.constants import ASC

from .base_service import BaseService


class CarService(BaseService):
    def __init__(self) -> None:
        self._car_repository = CarRepository()
        self.create_logger(__name__)

    def get_car(self, id_user: str, car_id: str) -> CarModel:
        self.logger.debug("Starting get_car")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug(f"Getting car <car_id: {car_id}> for <user: {id_user}>")

            hash_data = {"id_user": id_user, "car_id": car_id}
            hash_key = self.create_hash_key(hash_data)

            car_schema = self.get_user_cached_data(RedisDbsEnum.CARS, id_user, hash_key)

            if car_schema is None:
                car_schema = self._car_repository.select_car_by_id(db_session, id_user, car_id)

                self.insert_user_cache_data(RedisDbsEnum.CARS, id_user, hash_key, car_schema)

            return CarModel.model_validate(car_schema, from_attributes=True)

        except Exception as e:
            raise e

    def get_cars(
        self, id_user: str, query_filters: CarQueryFiltersModel, query_options: CarQueryOptionsModel
    ) -> CarQueryResponseModel:
        self.logger.debug("Starting get_cars")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Getting cars")

            query_filters_dict = query_filters.model_dump(exclude_none=True)
            query_options_dict = query_options.model_dump(exclude_none=True)
            hash_data = {**query_filters_dict, **query_options_dict, "id_user": id_user}
            hash_key = self.create_hash_key(hash_data)

            result_data = self.get_user_cached_data(RedisDbsEnum.CARS, id_user, hash_key)

            if result_data is None:
                cars_schemas: list[CarSchema] = self._car_repository.select_cars(
                    db_session,
                    id_user,
                    query_filters,
                    query_options,
                )

                count: int = self._get_cars_count(str(id_user), query_filters)

                offset = self.calculate_offset(query_options.per_page, query_options.page)

                result_data = dict(
                    results=cars_schemas,
                    metadata=dict(
                        sort_by=query_options.sort_by or "id_car",
                        sort_order=query_options.sort_order or ASC,
                        #
                        page=query_options.page or 1,
                        per_page=query_options.per_page or 10,
                        total_pages=self.calculate_max_pages(count, query_options.per_page or 10),
                        #
                        first_index=offset + 1,
                        last_index=offset + len(cars_schemas),
                        total_results=count,
                    ),
                )

                self.insert_user_cache_data(RedisDbsEnum.CARS, id_user, hash_key, result_data)

            return CarQueryResponseModel.model_validate(result_data)

        except Exception as e:
            raise e

    def create_car(self, id_user: uuid.UUID, new_car: CarNewModel) -> CarModel:
        self.logger.debug("Starting create_car")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Creating car for <user: {id_user}>")
            id_car = self._car_repository.insert_car(db_session, id_user, new_car)

            db_session.commit()

            car = self.get_car(str(id_user), id_car)

            self.reset_cache(str(id_user))

            return car

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def update_car(self, id_user: str, car_id: str, car_updates: CarUpdatesDataModel) -> CarModel:
        self.logger.debug("Starting update_car")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Updating car <car_id: {car_id}> of <user: {id_user}>")
            self._car_repository.update_car(db_session, id_user, car_id, car_updates)

            car_schema: CarSchema = self._car_repository.select_car_by_id(db_session, id_user, car_id)

            db_session.commit()

            self.reset_cache(str(id_user))

            return CarModel.model_validate(car_schema, from_attributes=True)

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

            self.reset_cache(str(id_user))

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def _get_cars_count(self, id_user: str, query_filters: CarQueryFiltersModel) -> int:
        self.logger.debug("Starting get_cars_count")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Getting cars count")

            cars_count = self._car_repository.count_cars(db_session, id_user, query_filters)

            return cars_count

        except Exception as e:
            raise e
