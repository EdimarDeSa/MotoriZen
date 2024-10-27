import os
import uuid

from keycloak import KeycloakAdmin, KeycloakError

from db.Models import UserModel, UserNewModel, UserUpdatesModel
from db.Schemas import UserSchema
from Enums import MotoriZenErrorEnum, RedisDbsEnum
from ErrorHandler import MotoriZenError
from Repositories.user_repository import UserRepository
from Services.base_service import BaseService
from Utils.redis_handler import RedisHandler


class UserService(BaseService):
    def __init__(self) -> None:
        self._admin = KeycloakAdmin(
            server_url=os.getenv("KC_URL"),
            username=os.getenv("KC_USER"),
            password=os.getenv("KC_PASSWORD"),
            client_id=os.getenv("KC_CLIENT_ID"),
            client_secret_key=os.getenv("KC_CLIENT_SECRET_KEY"),
            realm_name=os.getenv("KC_REALM"),
            verify=True,
        )
        self._user_repository = UserRepository()
        self._cache_handler = RedisHandler()
        self.create_logger(__name__)

    def get_user_by_cd_auth(self, cd_auth: str) -> UserModel:
        self.logger.debug("Starting select_user_by_cd_auth")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Getting user by cd_auth")
            user_data: UserSchema = self._user_repository.select_user_by_cd_auth(db_session, cd_auth)

            return UserModel.model_validate(user_data, from_attributes=True)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=repr(e), headers=None)

            raise e

        finally:
            db_session.close()

    def create_user(self, new_user: UserNewModel) -> None:
        self.logger.debug("Starting insert_user")
        db_session = self.create_session(write=True)
        cd_auth = None

        try:
            self.logger.debug(new_user)
            cd_auth = self._create_user_auth(new_user.email, new_user.first_name, new_user.last_name, new_user.password)

            self.logger.debug("Creating user data")
            new_user_data = UserSchema(cd_auth=cd_auth, **new_user.model_dump(exclude_none=True, exclude={"password"}))

            self.logger.debug("Inserting user data")
            self._user_repository.insert_user(db_session, new_user_data)

            db_session.commit()
            self.logger.debug("Session committed")

        except Exception as e:
            self.logger.exception(e)
            if cd_auth is not None:
                self._delete_user_auth(cd_auth)

            db_session.rollback()
            self.logger.debug("Rollbacked")

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=repr(e), headers=None)

            raise e

        finally:
            db_session.close()

    def update_user(self, id_user: uuid.UUID, update_user: UserUpdatesModel) -> UserModel:
        self.logger.debug("Starting update_user")
        db_session = self.create_session(write=True)

        try:
            self._user_repository.update_user(db_session, str(id_user), update_user)
            db_session.commit()

            self.logger.debug("Retrieving user data")
            user_data: UserSchema = self._user_repository.select_user_by_id(db_session, str(id_user))

            self.logger.debug("Updating user data in cache")

            self._cache_handler.set_data(
                RedisDbsEnum.USERS,
                str(user_data.cd_auth),
                user_data.as_dict(exclude_none=True),
            )

            self.logger.debug("User data retrieved")
            return UserModel.model_validate(user_data, from_attributes=True)

        except Exception as e:
            db_session.rollback()
            self.logger.debug("Rollbacked")

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=repr(e), headers=None)

            raise e

        finally:
            db_session.close()

    def remove_user(self, email: str, cd_auth: str) -> None:
        from Services.auth_service import AuthService

        self.logger.debug("Starting delete_user")
        db_session = self.create_session(write=True)

        try:
            AuthService().logout_user(email, str(cd_auth))

            self._delete_user_auth(cd_auth)
            self._user_repository.delete_user(db_session, email)
            db_session.commit()

            self._cache_handler.delete_data(RedisDbsEnum.USERS, cd_auth)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=repr(e), headers=None)

            raise e

        finally:
            db_session.close()

    def _create_user_auth(self, email: str, first_name: str, last_name: str, password: str) -> str:
        self.logger.debug("Creating user in Keycloak")
        try:
            cd_auth = self._admin.create_user(
                {
                    "email": email,
                    "username": email,
                    "enabled": True,
                    "firstName": first_name,
                    "lastName": last_name,
                    "emailVerified": True,
                    "credentials": [
                        {
                            "value": password,
                            "type": "password",
                            "temporary": False,
                        }
                    ],
                }
            )
            self.logger.debug(f"User created: {cd_auth}")

            return cd_auth

        except KeycloakError as e:
            match e.response_code:
                case 409:
                    raise MotoriZenError(
                        err=MotoriZenErrorEnum.USER_ALREADY_EXISTS,
                        detail=e.error_message,
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                case _:
                    raise MotoriZenError(
                        err=MotoriZenErrorEnum.UNKNOWN_ERROR,
                        detail=repr(e),
                    )

        except Exception as e:
            raise e

    def _delete_user_auth(self, cd_auth: str) -> None:
        try:
            self.logger.debug("Deleting user in Keycloak")
            self._admin.delete_user(cd_auth)
            self.logger.debug(f"User deleted: {cd_auth}")
        except KeycloakError as e:
            match e.response_code:
                case 400:
                    raise MotoriZenError(
                        err=MotoriZenErrorEnum.USER_NOT_FOUND,
                        detail=e.error_message,
                    )
                case _:
                    raise MotoriZenError(
                        err=MotoriZenErrorEnum.UNKNOWN_ERROR,
                        detail=repr(e),
                    )

        except Exception as e:
            raise e

    def _update_user_auth(
        self, id_auth: str, email_update: bool, email: str, name: str, surname: str
    ) -> dict[str, str]:
        try:
            payload: dict[str, str | bool] = {
                "email": email,
                "firstName": name,
                "lastName": surname,
            }

            if email_update is True:
                payload["emailVerified"] = False

            response: dict[str, str] = self._admin.update_user(user_id=id_auth, payload=payload)
            return response

        except KeycloakError as e:
            match e.response_code:
                case 400:
                    raise MotoriZenError(
                        err=MotoriZenErrorEnum.USER_NOT_FOUND,
                        detail=e.error_message,
                    )
                case _:
                    raise MotoriZenError(
                        err=MotoriZenErrorEnum.UNKNOWN_ERROR,
                        detail=repr(e),
                    )

        except Exception as e:
            raise e
