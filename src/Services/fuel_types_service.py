from DB.Models import FuelTypeModel
from DB.Schemas import FuelTypeSchema
from Enums import RedisDbsEnum
from Repositories.fuel_type_repository import FuelTypeRepository

from .base_service import BaseService


class FuelTypesService(BaseService):
    def __init__(self) -> None:
        self._fuel_type_repository = FuelTypeRepository()
        self.create_logger(__name__)

    def get_fuel_types(self) -> list[FuelTypeModel]:
        self.logger.debug("Starting get_fuel_types")
        db_session = self.create_session(write=False)

        try:
            hash_data = {"get_fuel_types": "all_fuel_types"}
            hash_key = self.create_hash_key(hash_data)

            fuel_type_schema_list = self.cache_handler.get_data(RedisDbsEnum.FUEL_TYPES, hash_key)

            if fuel_type_schema_list is None:
                self.logger.debug("Geting all fuel types")
                fuel_type_schema_list = self._fuel_type_repository.select_fuel_types(db_session)

                fuel_type_list = [schema.as_dict(exclude_none=True) for schema in fuel_type_schema_list]

                self.cache_handler.set_data(RedisDbsEnum.FUEL_TYPES, hash_key, fuel_type_list)

            return [
                FuelTypeModel.model_validate(fuel_type_schema, from_attributes=True)
                for fuel_type_schema in fuel_type_schema_list
            ]

        except Exception as e:
            raise e

        finally:
            db_session.close()

    def get_fuel_type(self, id_fuel_type: int) -> FuelTypeModel:
        self.logger.debug("Starting get_fuel_type")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug(f"Geting fuel type with id: {id_fuel_type}")

            hash_data = {"get_fuel_type": id_fuel_type}
            hash_key = self.create_hash_key(hash_data)

            fuel_type_schema = self.cache_handler.get_data(RedisDbsEnum.FUEL_TYPES, hash_key)

            if fuel_type_schema is None:
                self.logger.debug("Geting fuel type")
                fuel_type_schema = self._fuel_type_repository.select_fuel_type(db_session, id_fuel_type)

                self.cache_handler.set_data(RedisDbsEnum.FUEL_TYPES, hash_key, fuel_type_schema)

            return FuelTypeModel.model_validate(fuel_type_schema, from_attributes=True)

        except Exception as e:
            raise e

        finally:
            db_session.close()
