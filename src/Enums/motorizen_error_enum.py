from enum import IntEnum


class MotorizenErrorEnum(IntEnum):
    USER_NOT_FOUND = -100
    USER_ALREADY_EXISTS = -101

    LOGIN_ERROR = -200

    UNKNOWN_ERROR = -999

    def __repr__(self) -> str:
        return super().__repr__()
