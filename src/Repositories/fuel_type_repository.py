from sqlalchemy.orm import Session, scoped_session

from DB.Querys import FuelTypeQueryManager
from DB.Schemas import FuelTypeSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError

from .base_repository import BaseRepository


class FuelTypeRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self._fuel_type_querys = FuelTypeQueryManager()

    def select_fuel_types(self, db_session: scoped_session[Session]) -> list[FuelTypeSchema]:
        self.logger.debug("Starting select_fuel_types")

        try:
            query = self._fuel_type_querys.select_fuel_types()

            self.logger.debug(f"Selecting all fuel types on table <Table: {FuelTypeSchema.__tablename__}>")
            fuel_types_schema: list[FuelTypeSchema] | None = list(db_session.execute(query).scalars().all())

            if fuel_types_schema is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.FUEL_TYPE_NOT_FOUND, detail="Fuel types not found")

            self.logger.debug(f"Fuel types selected")

            return fuel_types_schema

        except Exception as e:
            raise e

    def select_fuel_type(self, db_session: scoped_session[Session], id_fuel_type: int) -> FuelTypeSchema:
        self.logger.debug("Starting select_fuel_type")

        try:
            query = self._fuel_type_querys.select_fuel_type(id_fuel_type)

            self.logger.debug(
                f"Selecting fuel type <id_fuel_type: {id_fuel_type}> on table <Table: {FuelTypeSchema.__tablename__}>"
            )
            fuel_type_schema: FuelTypeSchema | None = db_session.execute(query).scalar()

            if fuel_type_schema is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.FUEL_TYPE_NOT_FOUND, detail=f"Fuel type not found with id: {id_fuel_type}"
                )

            self.logger.debug(f"Fuel type selected <name: {fuel_type_schema.name}>")

            return fuel_type_schema

        except Exception as e:
            raise e
