from enum import Enum

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class ErrorData:
    status_code: int
    rc: int


class MotoriZenErrorEnum(Enum):
    USER_NOT_ACTIVE = ErrorData(403, -100)
    USER_NOT_FOUND = ErrorData(404, -104)
    USER_ALREADY_EXISTS = ErrorData(409, -109)
    TOKEN_EXPIRED = ErrorData(401, -110)

    LOGIN_ERROR = ErrorData(401, -200)
    LOGOUT_ERROR = ErrorData(401, -201)

    CAR_NOT_FOUND = ErrorData(404, -300)
    BRAND_NOT_FOUND = ErrorData(404, -301)
    REGISTER_NOT_FOUND = ErrorData(404, -302)
    INVALID_UPDATES_DATA = ErrorData(400, -310)
    INVALID_REGISTER_DATA = ErrorData(400, -311)

    INVALID_SORT_KEY = ErrorData(400, -800)

    UNKNOWN_ERROR = ErrorData(500, -999)

    def __repr__(self) -> str:
        return super().__repr__()
