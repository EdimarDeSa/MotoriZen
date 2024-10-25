import uuid
from typing import Any

from sqlalchemy import Delete, Insert, Select, Update
from sqlalchemy.orm import Session, scoped_session

from db.Models import UserUpdatesModel
from db.Schemas import UserSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self) -> None:
        self.create_logger(__name__)

    def select_user_by_id(self, db_session: scoped_session[Session], id_user: str) -> UserSchema:
        self.logger.debug("Starting select_user_by_id")

        try:
            query: Select[tuple[UserSchema]] = self.querys.select_user_by_id(id_user)

            self.logger.debug("Getting user by id")
            user_data: UserSchema | None = db_session.execute(query).scalar()

            if user_data is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.USER_NOT_FOUND, detail=f"User not found with id: {id_user}")

            return user_data

        except Exception as e:
            raise e

    def select_user_by_cd_auth(self, db_session: scoped_session[Session], cd_auth: str) -> UserSchema:
        self.logger.debug("Starting select_user_by_cd_auth")

        try:
            query: Select[tuple[UserSchema]] = self.querys.select_user_by_cd_auth(cd_auth)

            self.logger.debug("Getting user by cd_auth")
            user_data: UserSchema | None = db_session.execute(query).scalar()

            if user_data is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.USER_NOT_FOUND, detail=f"User not found with cd_auth: {cd_auth}"
                )

            return user_data

        except Exception as e:
            raise e

    def insert_user(self, db_session: scoped_session[Session], new_user_data: UserSchema) -> None:
        self.logger.debug("Starting insert_user")

        try:
            new_data: dict[str, Any] = new_user_data.as_dict(exclude_none=True)

            query: Insert = self.querys.insert_user(new_data)

            self.logger.debug("Inserting new user")
            result = db_session.execute(query)
            self.logger.debug(f"User inserted: {result.inserted_primary_key[0]}")

        except Exception as e:
            raise e

    def update_user(self, db_session: scoped_session[Session], id_user: str, update_user: UserUpdatesModel) -> None:
        self.logger.debug("Starting update_user")

        try:
            new_data: dict[str, Any] = update_user.model_dump(exclude_none=True)

            query: Update = self.querys.update_user(id_user, new_data)

            self.logger.debug(f"Updating user: {id_user}")
            db_session.execute(query)
            self.logger.debug("User updated")

        except Exception as e:
            raise e

    def delete_user(self, db_session: scoped_session[Session], email: str) -> None:
        self.logger.debug("Starting delete_user")

        try:
            query: Delete = self.querys.delete_user(email)

            self.logger.debug("Deleting user")
            db_session.execute(query)
            self.logger.debug("User deleted")

        except Exception as e:
            raise e
