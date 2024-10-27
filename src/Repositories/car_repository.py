import uuid
from typing import Any

from sqlalchemy.orm import Session, scoped_session

from db.Models import CarNewModel, CarQueryOptionsModel, CarUpdatesDataModel
from db.Schemas import BrandSchema, CarSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError

from .base_repository import BaseRepository


class CarRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)

    def select_car_by_id(self, db_session: scoped_session[Session], id_user: str, car_id: str) -> CarSchema:
        self.logger.debug("Starting select_car_by_id")

        try:
            query = self.querys.select_car_by_id(id_user, car_id)

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
        query_params_dict: dict[str, Any],
        query_options: CarQueryOptionsModel,
    ) -> list[CarSchema]:
        self.logger.debug("Starting select_cars")

        try:
            query = self.querys.select_cars(id_user, query_params_dict, query_options)

            self.logger.debug("Selecting cars")
            result: list[CarSchema] = list(db_session.execute(query).scalars().all())

            return result

        except Exception as e:
            raise e

    def select_cars_count(
        self, db_session: scoped_session[Session], id_user: str, query_params_dict: dict[str, Any]
    ) -> int:
        self.logger.debug("Starting select_cars_count")

        try:
            query = self.querys.select_cars_count(id_user, query_params_dict)

            self.logger.debug("Selecting cars count")
            result: int | None = db_session.execute(query).scalar()

            if result is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.CAR_NOT_FOUND, detail="Any car found")

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
            query = self.querys.insert_car(car_data)

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
            query = self.querys.update_car(id_user, id_car, car_updates_data)

            self.logger.debug(f"Updating car <car_id: {id_car}> on table <Table: {CarSchema.__tablename__}>")
            db_session.execute(query)

            self.logger.debug(f"Car updated <car_id: {id_car}>")

        except Exception as e:
            raise e

    def delete_car(self, db_session: scoped_session[Session], id_user: str, id_car: str) -> None:
        self.logger.debug("Starting delete_car")

        try:
            query = self.querys.delete_car(id_user, id_car)

            self.logger.debug(f"Deleting car <car_id: {id_car}> on table <Table: {CarSchema.__tablename__}>")
            db_session.execute(query)

            self.logger.debug(f"Car deleted <car_id: {id_car}>")

        except Exception as e:
            raise e

    def select_brands(self, db_session: scoped_session[Session]) -> list[BrandSchema]:
        self.logger.debug("Starting select_brand")

        try:
            query = self.querys.select_brands()

            self.logger.debug(f"Selecting all brands on table <Table: {BrandSchema.__tablename__}>")
            brand_schema: list[BrandSchema] | None = list(db_session.execute(query).scalars().all())

            if brand_schema is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.BRAND_NOT_FOUND, detail=f"Brand not faound with id: {id_brand}"
                )

            self.logger.debug(f"Brands selected")

            return brand_schema

        except Exception as e:
            raise e

    def select_brand(self, db_session: scoped_session[Session], id_brand: int) -> BrandSchema:
        self.logger.debug("Starting select_brand")

        try:
            query = self.querys.select_brand(id_brand)

            self.logger.debug(f"Selecting brand <id_brand: {id_brand}> on table <Table: {BrandSchema.__tablename__}>")
            brand_schema: BrandSchema | None = db_session.execute(query).scalar()

            if brand_schema is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.BRAND_NOT_FOUND, detail=f"Brand not faound with id: {id_brand}"
                )

            self.logger.debug(f"Brand selected <name: {brand_schema.name}>")

            return brand_schema

        except Exception as e:
            raise e
