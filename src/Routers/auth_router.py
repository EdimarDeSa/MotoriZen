from fastapi import APIRouter, Request

from db.Models import TokenModel
from Enums.motorizen_error_enum import MotorizenErrorEnum
from ErrorHandler import MotorizenError
from Services.auth_service import AuthService
from Utils.custom_types import PasswordRequestForm

from .base_router import BaseRouter


class AuthRouter(BaseRouter):
    def __init__(self) -> None:
        self.create_logger(__name__)
        self.router = APIRouter(tags=["Auth"], prefix="/token")
        self.auth_service = AuthService()

        self._register_routes()

    def _register_routes(self) -> None:
        # POST
        self.router.add_api_route("", self.login, response_model=TokenModel, methods=["POST"])
        # self.router.add_api_route("/refresh", self.refresh_token, methods=["POST"])

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
            --url http://localhost:8080/token \\
            --header 'Content-Type: multipart/form-data' \\
            --form username={email@domain.com} \\
            --form password={P@s5W0rd}
        """
        self.logger.info("Starting login")

        user_email = form_data.username
        password = form_data.password

        try:
            self.logger.debug(f"Try login with <Email: {user_email}>")
            token_: TokenModel = self.auth_service.authenticate_user(user_email, password)
            self.logger.info(f"Success login - token created - <token: {token_.access_token}>")

            return token_

        except Exception as e:
            self.logger.error(e)
            raise MotorizenError(
                err=MotorizenErrorEnum.LOGIN_ERROR, detail=repr(e), headers={"WWW-Authenticate": "Bearer"}
            ).as_http_response()
