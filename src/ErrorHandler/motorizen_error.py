from fastapi import HTTPException

from Contents.exception_content import ExceptionContent
from Enums import MotorizenErrorEnum
from ErrorHandler import ErrorModel


class MotorizenError(Exception):
    def __init__(
        self,
        err: MotorizenErrorEnum,
        detail: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.err = err
        self.detail = detail
        self.headers = headers
        super().__init__(f"<{self.err.name}: {self.err.value}>: {detail}")

    def as_http_response(self) -> HTTPException:
        error_model = ErrorModel(
            error=self.err.name,
            description=self.detail,
        )
        content = ExceptionContent(
            rc=self.err,
            data=error_model,
        )
        status_code = self.__cehck_error_code()
        return HTTPException(
            status_code=status_code,
            detail=content,
            headers=self.headers,
        )

    def __cehck_error_code(self) -> int:
        match self.err.value:
            case MotorizenErrorEnum.USER_NOT_FOUND:
                return 404
            case MotorizenErrorEnum.USER_ALREADY_EXISTS:
                return 409
            case MotorizenErrorEnum.LOGIN_ERROR:
                return 401
            case (
                MotorizenErrorEnum.ROUTERS_NOT_INITIALIZED
                | MotorizenErrorEnum.INVALID_ROUTER
                | MotorizenErrorEnum.LOGGER_NOT_INITIALIZED
            ):
                return 500
            case _:
                return 500
