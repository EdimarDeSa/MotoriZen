import uuid
from typing import Any

from sqlalchemy.orm import Session, scoped_session

from DB.Models import CarNewModel, CarQueryFiltersModel, CarQueryOptionsModel, CarUpdatesDataModel
from DB.Querys import CarQueryManager
from DB.Querys.user_query_manager import UserQueryManager
from DB.Schemas import BrandSchema, CarSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError

from .base_repository import BaseRepository


class CarRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self._car_querys = CarQueryManager()
        self._user_querys = UserQueryManager()

    def select_car_by_id(self, db_session: scoped_session[Session], id_user: str, car_id: str) -> CarSchema:
        self.logger.debug("Starting select_car_by_id")

        try:
            query = self._user_querys.select_user_data_by_id(CarSchema, id_user, car_id)

            self.logger.debug(f"Selecting car <car_id: {car_id}> for <user: {id_user}>")
            result: CarSchema | None = db_session.execute(query).scalar()

            if result is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.CAR_NOT_FOUND, detail="Car not found")

            return result

        except Exception as e:
            raise e

    def select_cars(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        query_filters: CarQueryFiltersModel,
        query_options: CarQueryOptionsModel,
    ) -> list[CarSchema]:
        self.logger.debug("Starting select_cars")

        try:
            query = self._user_querys.select_filtered_user_data(CarSchema, id_user, query_filters, query_options)

            self.logger.debug("Selecting cars")
            result: list[CarSchema] = list(db_session.execute(query).scalars().all())

            return result

        except Exception as e:
            raise e

    def count_cars(self, db_session: scoped_session[Session], id_user: str, query_filters: CarQueryFiltersModel) -> int:
        self.logger.debug("Starting select_cars_count")

        try:
            query = self._user_querys.count_total_results(CarSchema, id_user, query_filters)

            self.logger.debug("Selecting cars count")
            result: int | None = db_session.execute(query).scalar()

            if result is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.CAR_NOT_FOUND, detail="Any car found")

            return result

        except Exception as e:
            raise e

    def get_last_odometer(self, db_session: scoped_session[Session], id_user: str, id_car: str) -> float:
        self.logger.debug("Starting get_last_odometer")

        try:
            query = self._car_querys.select_last_odometer(id_user, id_car)

            self.logger.debug("Getting last odometer")
            result: float | None = db_session.execute(query).scalar()

            if result is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.CAR_NOT_FOUND, detail=f"Car not found with id: {id_car}")

            return result

        except Exception as e:
            raise e

    def insert_car(self, db_session: scoped_session[Session], id_user: uuid.UUID, new_car: CarNewModel) -> None:
        self.logger.debug("Starting create_car")

        try:
            car_data = CarSchema(
                cd_user=id_user,
                **new_car.model_dump(exclude_none=True),
            ).as_dict(exclude_none=True)
            query = self._user_querys.insert_data(CarSchema, car_data)

            self.logger.debug(f"Inserting car on table <Table: {CarSchema.__tablename__}>")
            result = db_session.execute(query)

            self.logger.debug(f"Car inserted <car_id; {result.inserted_primary_key[0]}>")

        except Exception as e:
            raise e

    def update_car(
        self, db_session: scoped_session[Session], id_user: str, id_car: str, car_updates: CarUpdatesDataModel
    ) -> None:
        self.logger.debug("Starting update_car")

        try:
            car_updates_data = car_updates.model_dump(exclude_none=True)
            query = self._user_querys.update_user_data(CarSchema, id_user, id_car, car_updates_data)

            self.logger.debug(f"Updating car <car_id: {id_car}> on table <Table: {CarSchema.__tablename__}>")
            db_session.execute(query)

            self.logger.debug(f"Car updated <car_id: {id_car}>")

        except Exception as e:
            raise e

    def update_car_odometer(
        self, db_session: scoped_session[Session], id_user: str, id_car: str, odometer: float
    ) -> None:
        self.logger.debug("Starting update_car_odometer")

        try:
            query = self._car_querys.update_car_odometer(id_user, id_car, odometer)

            self.logger.debug(f"Updating car <car_id: {id_car}> on table <Table: {CarSchema.__tablename__}>")
            db_session.execute(query)

            self.logger.debug(f"Car updated <car_id: {id_car}>")

        except Exception as e:
            raise e

    def delete_car(self, db_session: scoped_session[Session], id_user: str, id_car: str) -> None:
        self.logger.debug("Starting delete_car")

        try:
            query = self._user_querys.delete_user_data(CarSchema, id_user, id_car)

            self.logger.debug(f"Deleting car <car_id: {id_car}> on table <Table: {CarSchema.__tablename__}>")
            db_session.execute(query)

            self.logger.debug(f"Car deleted <car_id: {id_car}>")

        except Exception as e:
            raise e
