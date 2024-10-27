import db
from db.Models.register_model import RegisterModel
from db.Models.register_new_model import RegisterNewModel
from db.Models.register_update_data_model import RegisterUpdateDataModel
from db.Schemas.register_schema import RegisterSchema
from Repositories.register_repository import RegisterRepository
from Services.base_service import BaseService
from Utils.redis_handler import RedisHandler


class RegisterService(BaseService):
    def __init__(self) -> None:
        self.create_logger(__name__)
        self._register_repository = RegisterRepository()
        self._cache_handler = RedisHandler()

    def get_register(self, id_user: str, id_register: str) -> RegisterModel:
        self.logger.debug("Starting get_registers")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug(f"Getting register <register_id: {id_register}> for <user: {id_user}>")

            register_schema: RegisterSchema = self._register_repository.select_register_by_id(
                db_session, id_user, id_register
            )

            register_model = RegisterModel.model_validate(register_schema, from_attributes=True)

            db_session.commit()

            return register_model

        except Exception as e:
            raise e

        finally:
            db_session.close()

    def create_register(self, id_user: str, new_register: RegisterNewModel) -> None:
        self.logger.debug("Starting create_register")
        db_session = self.create_session(write=True)

        try:
            self.logger.debug(f"Creating register for <user: {id_user}>")

            new_register_schema: RegisterSchema = RegisterSchema(
                cd_user=id_user,
                **new_register.model_dump(),
            )

            self._register_repository.insert_register(db_session, new_register_schema)

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
