import os
from typing import Annotated

from fastapi import Depends
from keycloak import KeycloakOpenID

from db.Models.token_model import TokenModel
from db.Models.user_model import UserModel
from Enums.motorizen_error_enum import MotorizenErrorEnum
from ErrorHandler.motorizen_error import MotorizenError
from Services.base_service import BaseService
from Services.user_service import UserService
from Utils.oauth_service import oauth2_scheme


class AuthService(BaseService):
    def __init__(self) -> None:
        self._open_id = KeycloakOpenID(
            server_url=os.getenv("KC_URL"),
            realm_name=os.getenv("KC_REALM"),
            client_id=os.getenv("KC_CLIENT_ID"),
            client_secret_key=os.getenv("KC_CLIENT_SECRET_KEY"),
            verify=True,
        )
        self.create_logger(__name__)

    def authenticate_user(self, email: str, password: str) -> TokenModel:
        self.logger.info("Starting authenticate_user")

        try:
            self.logger.debug("Authenticating user")
            token_dict = self._open_id.token(email, password)
            self.logger.debug("User authenticated")

            token = TokenModel(**token_dict)
            return token

        except Exception as e:
            self.logger.error(e)
            raise e

    async def get_current_active_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
        self.logger.debug("Starting get_current_active_user")
        user_service = UserService()

        try:
            self.logger.debug("Decoding token")
            token_data = self._open_id.decode_token(token)
            cd_auth = token_data["sub"]
            self.logger.debug(f"Token decoded: <cd_auth: {cd_auth}>")

            user_data: UserModel = user_service.get_user_by_cd_auth(cd_auth)

            return user_data

        except Exception as e:
            self.logger.error(e)
            raise MotorizenError(
                err=MotorizenErrorEnum.LOGIN_ERROR,
                detail=repr(e),
            )
