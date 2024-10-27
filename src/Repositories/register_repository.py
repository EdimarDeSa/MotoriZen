from typing import Any

from sqlalchemy import Insert
from sqlalchemy.orm import Session, scoped_session

from db.Schemas import RegisterSchema
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError

from .base_repository import BaseRepository


class RegisterRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)

    def select_register_by_id(
        self, db_session: scoped_session[Session], id_user: str, id_register: str
    ) -> RegisterSchema:
        self.logger.debug("Starting select_register_by_id")
        try:
            query = self.querys.select_register_by_id(id_user, id_register)

            self.logger.debug(f"Selecting register <register_id: {id_register}> for <user: {id_user}>")
            register_schema: RegisterSchema | None = db_session.execute(query).scalar()

            if register_schema is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.REGISTER_NOT_FOUND,
                    detail="Register not found",
                )

            return register_schema
        except Exception as e:
            raise e

    def insert_register(self, db_session: scoped_session[Session], new_register: RegisterSchema) -> None:
        self.logger.debug("Starting insert_register")

        try:
            query: Insert = self.querys.insert_register(new_register.as_dict(exclude_none=True))

            self.logger.debug("Inserting new register")
            result = db_session.execute(query)
            self.logger.debug(f"Register inserted: {result.inserted_primary_key[0]}")

        except Exception as e:
            raise e

    def update_register(
        self, db_session: scoped_session[Session], id_user: str, id_register: str, updates: dict[str, Any]
    ) -> None:
        self.logger.debug("Starting update_register")

        try:
            query = self.querys.update_register(id_user, id_register, updates)

            self.logger.debug(f"Updating register <register_id: {id_register}> for <user: {id_user}>")
            db_session.execute(query)

        except Exception as e:
            raise e
