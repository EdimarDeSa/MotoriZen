from enum import IntEnum


class RedisDbsEnum(IntEnum):
    """
    Redis databases enum.
    """

    USERS = 0
    TOKENS = 1
    CARS = 2
    REGISTERS = 3
    BRANDS = 4
    REPORTS = 5
    SESSIONS = 6
    FUEL_TYPES = 7
