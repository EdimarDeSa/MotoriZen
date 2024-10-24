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
        err_data = self.err.value
        error_model = ErrorModel(
            error=self.err.name,
            description=self.detail,
        )
        content = ExceptionContent(
            rc=err_data.rc,
            data=error_model,
        )
        status_code = err_data.status_code
        return HTTPException(
            status_code=status_code,
            detail=content.model_dump(exclude_none=True),
            headers=self.headers,
        )
