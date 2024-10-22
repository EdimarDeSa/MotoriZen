from enum import IntEnum


class MotoriZenErrorEnum(IntEnum):
    USER_NOT_ACTIVE = -100
    USER_NOT_FOUND = -104
    USER_ALREADY_EXISTS = -109
    TOKEN_EXPIRED = -110

    LOGIN_ERROR = -200
    LOGOUT_ERROR = -201

    UNKNOWN_ERROR = -999

    def __repr__(self) -> str:
        return super().__repr__()
