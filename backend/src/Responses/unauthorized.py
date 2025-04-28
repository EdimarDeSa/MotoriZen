from fastapi import HTTPException


class Unauthorized(HTTPException):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
    ) -> None:
        headers = {"WWW-Authenticate": "Bearer"} if headers is None else headers
        super().__init__(status_code=401, headers=headers, detail="Invalid user credentials")
