from fastapi import HTTPException

from Contents.exception_content import ExceptionContent


class Conflict(HTTPException):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
        detail: ExceptionContent | None = None,
    ) -> None:
        super().__init__(status_code=409, headers=headers, detail=detail)
