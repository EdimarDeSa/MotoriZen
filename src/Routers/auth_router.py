from fastapi import APIRouter, Request

from db.Models import TokenModel
from db.Models.refresh_token_model import RefreshTokenModel
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Responses.no_content import NoContent
from Services.auth_service import AuthService
from Utils.custom_types import CurrentActiveUser, PasswordRequestForm

from .base_router import BaseRouter


class AuthRouter(BaseRouter):
    def __init__(self) -> None:
        self.create_logger(__name__)
        self.router = APIRouter(tags=["Auth"])
        self.auth_service = AuthService()

        self._register_routes()

    def _register_routes(self) -> None:
        # POST
        self.router.add_api_route("/token", self.login, response_model=TokenModel, methods=["POST"])
        self.router.add_api_route("/refresh", self.refresh_token, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["GET"])

    async def login(
        self,
        request: Request,
        form_data: PasswordRequestForm,
    ) -> TokenModel:
        """
        Create a new token for the user.

        Attributes:

            form_data (PasswordRequestForm): As credenciais fornecidas pelo usuário.

        Example:

            $ curl -X POST \\
            --url http://localhost:8000/token \\
            --header 'Content-Type: multipart/form-data' \\
            --form username={email@domain.com} \\
            --form password={P@s5W0rd}
        """
        self.logger.info("Starting login")

        user_email = form_data.username
        password = form_data.password

        print(user_email, password)

        try:
            self.logger.debug(f"Try login with <Email: {user_email}>")
            token_: TokenModel = self.auth_service.authenticate_user(user_email, password)
            self.logger.info(f"Success login - token created - <token: {token_.access_token}>")

            return token_

        except Exception as e:
            self.logger.error(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=str(e))

            raise e.as_http_response()

    async def refresh_token(self, request: Request, refresh_token_model: RefreshTokenModel) -> TokenModel:
        """
        Refresh a token for the user.

        Args:

            refresh_token (RefreshTokenModel): Refresh token fornecido pelo /token.

        Example:

            $ curl -X POST \\
            --url http://localhost:8000/refresh \\
            --header 'Authorization: Bearer acess_token'
        """
        self.logger.info("Starting refresh_token")

        try:
            token_ = self.auth_service.refresh_token(refresh_token_model.refresh_token)

            return token_

        except Exception as e:
            self.logger.exception(e)
            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=str(e))

            raise e.as_http_response()

    async def logout(self, request: Request, user_data: CurrentActiveUser) -> NoContent:
        """
        Delete a token for the user.

        Example:

            $ curl -X POST \\
            --url http://localhost:8000/logout \\
            --header 'Authorization: Bearer acess_token'
        """
        self.logger.info("Starting logout")

        try:
            self.auth_service.logout_user(user_data.email, str(user_data.cd_auth))

            return NoContent()

        except Exception as e:
            self.logger.error(e)
            raise MotoriZenError(
                err=MotoriZenErrorEnum.LOGOUT_ERROR, detail=str(e), headers={"WWW-Authenticate": "Bearer"}
            ).as_http_response()
