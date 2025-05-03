import uuid

from db.Models import (
    VehicleModel,
    VehicleNewModel,
    VehicleQueryFiltersModel,
    VehicleQueryOptionsModel,
    VehicleQueryResponseModel,
    VehicleUpdatesDataModel,
)
from db.Schemas import VehicleSchema
from Enums import RedisDbsEnum
from Repositories.vehicle_repository import VehicleRepository
from Utils.constants import ASC

from .base_service import BaseService


class VehicleService(BaseService):
    def __init__(self) -> None:
        self._vehicle_repository = VehicleRepository()
        self.create_logger(__name__)

    def get_vehicle(self, id_user: str, vehicle_id: str) -> VehicleModel:
        self.logger.debug("Starting get_vehicle")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug(f"Getting vehicle <VEHICLE_ID: {vehicle_id}> for <user: {id_user}>")

            hash_data = {"id_user": id_user, "VEHICLE_ID": vehicle_id}
            hash_key = self.create_hash_key(hash_data)

            vehicle_schema = self.get_user_cached_data(RedisDbsEnum.VEHICLES, id_user, hash_key)

            if vehicle_schema is None:
                vehicle_schema = self._vehicle_repository.select_vehicle_by_id(db_session, id_user, vehicle_id)

                self.insert_user_cache_data(RedisDbsEnum.VEHICLES, id_user, hash_key, vehicle_schema)

            return VehicleModel.model_validate(vehicle_schema, from_attributes=True)

        except Exception as e:
            raise e

    def get_vehicles(
        self, id_user: str, query_filters: VehicleQueryFiltersModel, query_options: VehicleQueryOptionsModel
    ) -> VehicleQueryResponseModel:
        self.logger.debug("Starting get_vehicles")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Getting vehicles")

            query_filters_dict = query_filters.model_dump(exclude_none=True)
            query_options_dict = query_options.model_dump(exclude_none=True)
            hash_data = {**query_filters_dict, **query_options_dict, "id_user": id_user}
            hash_key = self.create_hash_key(hash_data)

            result_data = self.get_user_cached_data(RedisDbsEnum.VEHICLES, id_user, hash_key)

            if result_data is None:
                vehicles_schemas: list[VehicleSchema] = self._vehicle_repository.select_vehicles(
                    db_session,
                    id_user,
                    query_filters,
                    query_options,
                )

                count: int = self._get_vehicles_count(str(id_user), query_filters)

                offset = self.calculate_offset(query_options.per_page, query_options.page)

                result_data = dict(
                    results=vehicles_schemas,
                    metadata=dict(
                        sort_by=query_options.sort_by or "id_vehicle",
                        sort_order=query_options.sort_order or ASC,
                        #
                        page=query_options.page or 1,
                        per_page=query_options.per_page or 10,
                        total_pages=self.calculate_max_pages(count, query_options.per_page or 10),
                        #
                        first_index=offset + 1,
                        last_index=offset + len(vehicles_schemas),
                        total_results=count,
                    ),
                )

                self.insert_user_cache_data(RedisDbsEnum.VEHICLES, id_user, hash_key, result_data)

            return VehicleQueryResponseModel.model_validate(result_data)

        except Exception as e:
            raise e

    def create_vehicle(self, id_user: uuid.UUID, new_vehicle: VehicleNewModel) -> VehicleModel:
        self.logger.debug("Starting create_vehicle")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Creating vehicle for <user: {id_user}>")
            id_vehicle = self._vehicle_repository.insert_vehicle(db_session, id_user, new_vehicle)

            db_session.commit()

            vehicle = self.get_vehicle(str(id_user), id_vehicle)

            self.reset_cache(str(id_user))

            return vehicle

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def update_vehicle(self, id_user: str, vehicle_id: str, vehicle_updates: VehicleUpdatesDataModel) -> VehicleModel:
        self.logger.debug("Starting update_vehicle")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Updating vehicle <VEHICLE_ID: {vehicle_id}> of <user: {id_user}>")
            self._vehicle_repository.update_vehicle(db_session, id_user, vehicle_id, vehicle_updates)

            vehicle_schema: VehicleSchema = self._vehicle_repository.select_vehicle_by_id(
                db_session, id_user, vehicle_id
            )

            db_session.commit()

            self.reset_cache(str(id_user))

            return VehicleModel.model_validate(vehicle_schema, from_attributes=True)

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def delete_vehicle(self, id_user: str, vehicle_id: str) -> None:
        self.logger.debug("Starting delete_vehicle")
        db_session = self.create_session(write=True)
        # FUTURE: implmentar soft delete
        # FUTURE: implmentar campo para caso o usuário queira que os registros vinculados ao carro sejam deletados
        # BUG: Verificar melhor forma de manter os registros em caso de exclusão de veículos
        # Teremos problemas em atualizações de registros sem veículos vinculados
        # Atualmente o banco está como >>> "ON DELETE SET NULL" <<< Verificar se isso causa problemas
        # Pensei em criar um carro default de sistema para ser usado em caso de exclusão de veículos
        # Isso pode ser um problema pois o carro deveria ser uma REFERENCIA de carro do user

        try:
            self.logger.debug(f"Deleting vehicle <VEHICLE_ID: {vehicle_id}> of <user: {id_user}>")
            self._vehicle_repository.delete_vehicle(db_session, id_user, vehicle_id)

            db_session.commit()

            self.reset_cache(str(id_user))

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def _get_vehicles_count(self, id_user: str, query_filters: VehicleQueryFiltersModel) -> int:
        self.logger.debug("Starting get_vehicles_count")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Getting vehicles count")

            vehicles_count = self._vehicle_repository.count_vehicles(db_session, id_user, query_filters)

            return vehicles_count

        except Exception as e:
            raise e
