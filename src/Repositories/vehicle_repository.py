import uuid
from typing import Any

from sqlalchemy.orm import Session, scoped_session

from db.Models import VehicleNewModel, VehicleQueryFiltersModel, VehicleQueryOptionsModel, VehicleUpdatesDataModel
from db.Querys import VehicleQueryManager
from db.Querys.user_query_manager import UserQueryManager
from db.Schemas import VehicleSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError

from .base_repository import BaseRepository


class VehicleRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self._vehicle_querys = VehicleQueryManager()
        self._user_querys = UserQueryManager()

    def select_vehicle_by_id(self, db_session: scoped_session[Session], id_user: str, vehicle_id: str) -> VehicleSchema:
        self.logger.debug("Starting select_vehicle_by_id")

        try:
            query = self._user_querys.select_user_data_by_id(VehicleSchema, id_user, vehicle_id)

            self.logger.debug(f"Selecting vehicle <vehicle_id: {vehicle_id}> for <user: {id_user}>")
            result: VehicleSchema | None = db_session.execute(query).scalar()

            if result is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.VEHICLE_NOT_FOUND, detail="Vehicle not found")

            return result

        except Exception as e:
            raise e

    def select_vehicles(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        query_filters: VehicleQueryFiltersModel,
        query_options: VehicleQueryOptionsModel,
    ) -> list[VehicleSchema]:
        self.logger.debug("Starting select_vehicles")

        try:
            query = self._user_querys.select_filtered_user_data(VehicleSchema, id_user, query_filters, query_options)

            self.logger.debug("Selecting vehicles")
            result: list[VehicleSchema] = list(db_session.execute(query).scalars().all())

            return result

        except Exception as e:
            raise e

    def count_vehicles(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        query_filters: VehicleQueryFiltersModel,
    ) -> int:
        self.logger.debug("Starting select_vehicles_count")

        try:
            query = self._user_querys.count_total_results(VehicleSchema, id_user, query_filters)

            self.logger.debug("Selecting vehicles count")
            result: int | None = db_session.execute(query).scalar()

            if result is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.VEHICLE_NOT_FOUND, detail="Any vehicle found")

            return result

        except Exception as e:
            raise e

    def get_last_odometer(self, db_session: scoped_session[Session], id_user: str, id_vehicle: str) -> float:
        self.logger.debug("Starting get_last_odometer")

        try:
            query = self._vehicle_querys.select_last_odometer(id_user, id_vehicle)

            self.logger.debug("Getting last odometer")
            result: float | None = db_session.execute(query).scalar()

            if result is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.VEHICLE_NOT_FOUND, detail=f"Vehicle not found with id: {id_vehicle}"
                )

            return result

        except Exception as e:
            raise e

    def insert_vehicle(
        self,
        db_session: scoped_session[Session],
        id_user: uuid.UUID,
        new_vehicle: VehicleNewModel,
    ) -> str:
        self.logger.debug("Starting create_vehicle")

        try:
            vehicle_data = VehicleSchema(
                cd_user=id_user,
                **new_vehicle.model_dump(exclude_none=True),
            ).as_dict(exclude_none=True)
            query = self._user_querys.insert_data(VehicleSchema, vehicle_data)

            self.logger.debug(f"Inserting vehicle on table <Table: {VehicleSchema.__tablename__}>")
            result = db_session.execute(query)

            self.logger.debug(f"Vehicle inserted <VEHICLE_ID; {result.inserted_primary_key[0]}>")

            return str(result.inserted_primary_key[0])

        except Exception as e:
            raise e

    def update_vehicle(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        id_vehicle: str,
        vehicle_updates: VehicleUpdatesDataModel,
    ) -> None:
        self.logger.debug("Starting update_vehicle")

        try:
            vehicle_updates_data = vehicle_updates.model_dump(exclude_none=True)
            query = self._user_querys.update_user_data(VehicleSchema, id_user, id_vehicle, vehicle_updates_data)

            self.logger.debug(
                f"Updating vehicle <VEHICLE_ID: {id_vehicle}> on table <Table: {VehicleSchema.__tablename__}>"
            )
            db_session.execute(query)

            self.logger.debug(f"Vehicle updated <VEHICLE_ID: {id_vehicle}>")

        except Exception as e:
            raise e

    def update_vehicle_odometer(
        self, db_session: scoped_session[Session], id_user: str, id_vehicle: str, odometer: float
    ) -> None:
        self.logger.debug("Starting update_vehicle_odometer")

        try:
            query = self._vehicle_querys.update_vehicle_odometer(id_user, id_vehicle, odometer)

            self.logger.debug(
                f"Updating vehicle <VEHICLE_ID: {id_vehicle}> on table <Table: {VehicleSchema.__tablename__}>"
            )
            db_session.execute(query)

            self.logger.debug(f"Vehicle updated <VEHICLE_ID: {id_vehicle}>")

        except Exception as e:
            raise e

    def delete_vehicle(self, db_session: scoped_session[Session], id_user: str, id_vehicle: str) -> None:
        self.logger.debug("Starting delete_vehicle")

        try:
            query = self._user_querys.delete_user_data(VehicleSchema, id_user, id_vehicle)

            self.logger.debug(
                f"Deleting vehicle <VEHICLE_ID: {id_vehicle}> on table <Table: {VehicleSchema.__tablename__}>"
            )
            db_session.execute(query)

            self.logger.debug(f"Vehicle deleted <VEHICLE_ID: {id_vehicle}>")

        except Exception as e:
            raise e
