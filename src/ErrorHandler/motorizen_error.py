from fastapi import HTTPException

from Contents.exception_content import ExceptionContent
from Enums import MotoriZenErrorEnum
from ErrorHandler import ErrorModel


class MotoriZenError(Exception):
    def __init__(
        self,
        err: MotoriZenErrorEnum,
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
            detail=content.model_dump(exclude_none=True),
            headers=self.headers,
        )

    def __cehck_error_code(self) -> int:
        match self.err.value:
            case MotoriZenErrorEnum.USER_NOT_FOUND:
                return 404
            case MotoriZenErrorEnum.USER_ALREADY_EXISTS:
                return 409
            case MotoriZenErrorEnum.LOGIN_ERROR:
                return 401
            case _:
                return 500
