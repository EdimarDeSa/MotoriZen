import os
from typing import Annotated, Any, Optional

from fastapi import Depends
from jwcrypto.jwt import JWTExpired
from keycloak import KeycloakOpenID

from DB.Models import TokenModel, UserModel
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from Enums.redis_dbs_enum import RedisDbsEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Services.base_service import BaseService
from Services.user_service import UserService
from Utils.oauth_service import oauth2_scheme
from Utils.redis_handler import RedisHandler


class AuthService(BaseService):
    def __init__(self) -> None:
        self._auth_handler = KeycloakOpenID(
            server_url=os.getenv("KC_URL"),
            realm_name=os.getenv("KC_REALM"),
            client_id=os.getenv("KC_CLIENT_ID"),
            client_secret_key=os.getenv("KC_CLIENT_SECRET_KEY"),
            verify=True,
        )
        self.create_logger(__name__)
        self._cache_handler = RedisHandler()

    def authenticate_user(self, email: str, password: str) -> TokenModel:
        self.logger.info("Starting authenticate_user")

        try:
            token_dict = self._get_token_from_cache(email)
            self.logger.debug(f"Token from cache service: {token_dict}")

            if token_dict is None:
                self.logger.debug("Token not found in cache. Authenticating with Keycloak.")

                token_dict = self._auth_handler.token(email, password)
                self.logger.debug(f"User authenticated - <TokenData: {token_dict}>")

                self._save_token_to_cache(email, token_dict)

            return TokenModel.model_validate(token_dict, from_attributes=True)

        except Exception as e:
            self.logger.error(e)
            raise e

    def _get_token_from_cache(self, email: str) -> dict[str, Any] | None:
        try:
            self.logger.debug(f"Getting token from cache for email: {email}")
            result = self._cache_handler.get_data(RedisDbsEnum.TOKENS, email)

            if isinstance(result, dict):
                return result
            return None

        except Exception as e:
            raise e

    def _save_token_to_cache(self, email: str, token_data: dict[str, Any]) -> None:
        try:
            exp = token_data.get("expires_in", None)
            self.logger.debug(f"Saving token to cache with expiration: {exp}")
            self._cache_handler.set_data(RedisDbsEnum.TOKENS, email, token_data, ex=exp)

        except Exception as e:
            raise e

    async def get_current_active_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
        self.logger.debug("Starting get_current_active_user")
        user_service = UserService()

        try:
            token_data = self._decode_token(token)

            cd_auth = token_data.get("sub", None)
            self.logger.debug(f"Token decoded: <cd_auth: {cd_auth}>")

            user_data = self._get_user_from_cache(cd_auth)
            self.logger.debug(f"User from cache service: <user_data: {user_data}>")

            user_model = None

            if user_data is None:
                self.logger.debug("Getting user from database")
                user_model = user_service.get_user_by_cd_auth(cd_auth)

                user_data = user_model.model_dump(mode="json", exclude_none=True)
                self.logger.debug(f"User from database: <user_data: {user_data}>")

                self._save_user_to_cache(cd_auth, user_data, token_data.get("expires_in", None))

            self._check_user_active(user_data)

            if user_model is None:
                user_model = UserModel.model_validate(user_data, from_attributes=True)

            return user_model

        except Exception as e:
            if not isinstance(e, MotoriZenError):
                raise MotoriZenError(err=MotoriZenErrorEnum.LOGIN_ERROR, detail=str(e))

            raise e

    def _decode_token(self, token: str) -> dict[str, Any]:
        try:
            self.logger.debug(f"Decoding <token: {token}>")
            return self._auth_handler.decode_token(token, validate=True)

        except Exception as e:
            if isinstance(e, JWTExpired):
                raise MotoriZenError(err=MotoriZenErrorEnum.TOKEN_EXPIRED, detail=str(e))
            raise e

    def _get_user_from_cache(self, cd_auth: str) -> dict[str, Any] | None:
        try:
            self.logger.debug(f"Getting user from cache for cd_auth: {cd_auth}")
            user_data = self._cache_handler.get_data(RedisDbsEnum.USERS, cd_auth)

            if isinstance(user_data, dict):
                return user_data

            return None

        except Exception as e:
            raise e

    def _save_user_to_cache(self, cd_auth: str, user_data: dict[str, Any], expires_in: Optional[int] = None) -> None:
        try:
            self.logger.debug(f"Saving user to cache for cd_auth: {cd_auth}")
            self._cache_handler.set_data(RedisDbsEnum.USERS, cd_auth, user_data, ex=expires_in)
            self.logger.debug("User saved in cache service")

        except Exception as e:
            raise e

    def _check_user_active(self, user_data: dict[str, Any]) -> None:
        self.logger.debug("Checking if user is active")

        if not user_data.get("is_active", False):
            raise MotoriZenError(
                err=MotoriZenErrorEnum.USER_NOT_ACTIVE,
                detail="The user is not active",
            )

    def refresh_token(self, refresh_token: str) -> TokenModel:
        self.logger.debug("Starting refresh_token")
        try:
            token_data = self._auth_handler.refresh_token(refresh_token)

            return TokenModel.model_validate(token_data, from_attributes=True)

        except Exception as e:
            raise e

    def logout_user(self, email: str, cd_auth: str) -> None:
        self.logger.debug("Starting logout_user")

        try:
            token_dict = self._get_token_from_cache(email)

            if token_dict is not None:
                self._auth_handler.logout(token_dict.get("refresh_token", None))

            self._cache_handler.delete_data(RedisDbsEnum.TOKENS, email)
            self._cache_handler.delete_data(RedisDbsEnum.USERS, cd_auth)

            self.logger.debug("User logged out")

        except Exception as e:
            raise e
