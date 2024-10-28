from DB.Models import CarModel, RegisterModel, RegisterNewModel, RegisterNewResponseModel, RegisterUpdateDataModel
from DB.Models.register_query_filters_model import RegisterQueryFiltersModel
from DB.Models.register_query_options import RegisterQueryOptionsModel
from DB.Schemas import RegisterSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Repositories.car_repository import CarRepository
from Repositories.register_repository import RegisterRepository
from Services.base_service import BaseService
from Utils.redis_handler import RedisHandler


class RegisterService(BaseService):
    def __init__(self) -> None:
        self.create_logger(__name__)
        self._register_repository = RegisterRepository()
        self._car_repository = CarRepository()
        self._cache_handler = RedisHandler()

    def get_registers(
        self, id_user: str, query_filters: RegisterQueryFiltersModel, query_options: RegisterQueryOptionsModel
    ) -> list[RegisterModel]:
        self.logger.debug("Starting get_registers")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug(f"Getting registers for <user: {id_user}>")

            registers_schemas: list[RegisterSchema] = self._register_repository.select_registers(
                db_session, id_user, query_filters, query_options
            )

            # TODO: Colocar cache aqui
            # TODO: Criar função para a contagem de registros
            # TODO: Adicionar a quantidade de registros no retorno
            # TODO: Adicionar offset-page no retorno

            registers_models = [
                RegisterModel.model_validate(register_schema, from_attributes=True)
                for register_schema in registers_schemas
            ]

            return registers_models

        except Exception as e:
            raise e

        finally:
            db_session.close()

    def get_register(self, id_user: str, id_register: str) -> RegisterModel:
        self.logger.debug("Starting get_registers")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug(f"Getting register <register_id: {id_register}> for <user: {id_user}>")

            register_schema: RegisterSchema = self._register_repository.select_register_by_id(
                db_session, id_user, id_register
            )

            register_model = RegisterModel.model_validate(register_schema, from_attributes=True)

            return register_model

        except Exception as e:
            raise e

        finally:
            db_session.close()

    def create_register(self, id_user: str, new_register: RegisterNewModel) -> RegisterNewResponseModel:
        self.logger.debug("Starting create_register")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Creating register for <user: {id_user}>")

            new_register_data = new_register.model_dump()

            odometer_new = new_register_data.pop("odometer")
            odometer_old = self._car_repository.get_last_odometer(db_session, id_user, str(new_register.cd_car))
            distance: float = new_register_data.get("distance", 0.0)

            if odometer_old >= odometer_new:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.INVALID_REGISTER_DATA,
                    detail="Odometer cannot be lower than the last odometer.",
                )

            if odometer_new is not None and distance:
                self.logger.debug("Calculating distance")
                distance = odometer_new - odometer_old
                new_register_data["distance"] = distance

            if odometer_new is None and not distance:
                self.logger.debug("Calculating odometer")
                odometer_new = odometer_old + distance

            if (odometer_old + distance) >= odometer_new:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.INVALID_REGISTER_DATA,
                    detail="Last odometer + distance cannot be lower than the new odometer.",
                )

            self._car_repository.update_car_odometer(db_session, id_user, str(new_register.cd_car), odometer_new)

            new_register_schema: RegisterSchema = RegisterSchema(
                cd_user=id_user,
                **new_register_data,
            )

            id_register = self._register_repository.insert_register(db_session, new_register_schema)

            db_session.commit()

            register_model = self.get_register(id_user, id_register)
            car_schema = self._car_repository.select_car_by_id(db_session, id_user, str(new_register.cd_car))

            car_model = CarModel.model_validate(car_schema, from_attributes=True)

            return RegisterNewResponseModel(
                register_data=register_model,
                car_data=car_model,
            )

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()

    def update_register(self, id_user: str, id_register: str, updates: RegisterUpdateDataModel) -> None:
        self.logger.debug("Starting update_register")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Updating register <register_id: {id_register}> for <user: {id_user}>")

            updates_data = updates.model_dump(exclude_none=True)

            self._register_repository.update_register(db_session, id_user, id_register, updates_data)

            db_session.commit()

        except Exception as e:
            db_session.rollback()
            raise e

    def delete_register(self, id_user: str, id_register: str) -> None:
        self.logger.debug("Starting delete_register")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Deleting register <register_id: {id_register}> for <user: {id_user}>")

            self._register_repository.delete_register(db_session, id_user, id_register)

            db_session.commit()

        except Exception as e:
            db_session.rollback()
            raise e

        finally:
            db_session.close()
