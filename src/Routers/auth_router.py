from fastapi import APIRouter, Request
from DB.Models import CsrfToken, RefreshTokenModel, TokenModel
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Responses import NoContent
from Services.auth_service import AuthService
from Utils.custom_types import CurrentActiveUser, PasswordRequestForm

from .base_router import BaseRouter

X_CSRF_TOKEN = "X-CSRF-Token"


class AuthRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(tags=["Auth"])
        self.auth_service = AuthService()

        self._register_routes()

    def _register_routes(self) -> None:
        # POST
        self.router.add_api_route("/token", self.login, response_model=TokenModel, methods=["POST"])
        self.router.add_api_route("/token/refresh", self.refresh_token, methods=["POST"])
        self.router.add_api_route("/token/logout", self.logout, methods=["GET"])
        self.router.add_api_route("/get-csrf-token", self.get_csrf_token, methods=["GET"])

    def _is_swagger_request(self, request: Request) -> bool:
        origin = request.headers.get("origin", "")
        return origin == "http://localhost:8000"

    async def login(
        self,
        request: Request,
        form_data: PasswordRequestForm,
    ) -> TokenModel:
        """
        Create a new token for the user with CSRF protection.

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

        try:

            if self._is_swagger_request(request):
                self.logger.info("Request from Swagger UI")
            else:
                session_token = request.session.pop(X_CSRF_TOKEN)
                self.logger.debug(f"Session token: {session_token}")

                header_token = request.headers.get(X_CSRF_TOKEN, None)
                self.logger.debug(f"Header token: {header_token}")

                self.auth_service.validate_csrf_token(header_token, session_token)

            user_email = form_data.username
            password = form_data.password

            self.logger.debug(f"Try login with <Email: {user_email}>")
            token_: TokenModel = self.auth_service.authenticate_user(user_email, password)
            self.logger.info(f"Success login - token created - <token: {token_.access_token}>")

            return token_

        except Exception as e:
            self.logger.error(e)
            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=str(e))
            raise e.as_http_response()

    async def refresh_token(
        self,
        request: Request,
        refresh_token_model: RefreshTokenModel,
    ) -> TokenModel:
        """
        Refresh a token for the user.

        Args:

            refresh_token (RefreshTokenModel): Refresh token fornecido pelo /token.

        Example:

            $ curl -X POST \\
            --url http://localhost:8000/refresh \\
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

    async def get_csrf_token(self, request: Request) -> CsrfToken:
        self.logger.info("Starting get_csrf_token")
        try:
            token = self.auth_service.generate_csrf_token()

            self.logger.debug(f"Generated token: {token}")
            request.session[X_CSRF_TOKEN] = token
            self.logger.debug(f"Request session: {request.session.__dict__}")

            return CsrfToken(csrf_token=token)

        except Exception as e:
            self.logger.error(e)
            raise MotoriZenError(
                err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail=str(e), headers={X_CSRF_TOKEN: ""}
            ).as_http_response()
