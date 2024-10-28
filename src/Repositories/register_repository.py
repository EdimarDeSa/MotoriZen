from typing import Any

from sqlalchemy import Insert
from sqlalchemy.orm import Session, scoped_session

from DB.Models.register_query_filters_model import RegisterQueryFiltersModel
from DB.Models.register_query_options import RegisterQueryOptionsModel
from DB.Schemas import RegisterSchema
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError

from .base_repository import BaseRepository


class RegisterRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)

    def select_registers(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        query_filters: RegisterQueryFiltersModel,
        query_options: RegisterQueryOptionsModel,
    ) -> list[RegisterSchema]:
        self.logger.debug("Starting select_registers")

        try:
            query = self.querys.select_registers(id_user, query_filters, query_options)

            self.logger.debug(f"Selecting registers for <user: {id_user}>")
            registers_schemas: list[RegisterSchema] = list(db_session.execute(query).scalars().all())

            return registers_schemas
        except Exception as e:
            raise e

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

    def count_registers(
        self, db_session: scoped_session[Session], id_user: str, query_filters: RegisterQueryFiltersModel
    ) -> int:
        self.logger.debug("Starting count_registers")

        try:
            query = self.querys.count_total_results(RegisterSchema, id_user, query_filters)

            self.logger.debug(f"Counting registers for <user: {id_user}>")
            total_registers: int | None = db_session.execute(query).scalar()

            if total_registers is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.REGISTER_NOT_FOUND,
                    detail="Any register found with given filters",
                )

            return total_registers
        except Exception as e:
            raise e

    def insert_register(self, db_session: scoped_session[Session], new_register: RegisterSchema) -> str:
        self.logger.debug("Starting insert_register")

        try:
            query: Insert = self.querys.insert_register(new_register.as_dict(exclude_none=True))

            self.logger.debug("Inserting new register")
            result = db_session.execute(query)
            self.logger.debug(f"Register inserted: {result.inserted_primary_key[0]}")

            return result.inserted_primary_key[0]

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

    def delete_register(self, db_session: scoped_session[Session], id_user: str, id_register: str) -> None:
        self.logger.debug("Starting delete_register")

        try:
            query = self.querys.delete_register(id_user, id_register)

            self.logger.debug(f"Deleting register <register_id: {id_register}> for <user: {id_user}>")
            db_session.execute(query)

        except Exception as e:
            raise e
