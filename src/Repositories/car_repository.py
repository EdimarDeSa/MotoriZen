import uuid

from sqlalchemy.orm import Session, scoped_session

from db.Models.car_model import NewCarModel
from db.Schemas.car_schema import CarSchema
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError

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

    def insert_car(self, db_session: scoped_session[Session], id_user: uuid.UUID, new_car: NewCarModel) -> None:
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
