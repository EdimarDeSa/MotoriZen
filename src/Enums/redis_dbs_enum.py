from enum import IntEnum


class RedisDbsEnum(IntEnum):
    """
    Redis databases
    """

    USERS = 0
    TOKENS = 1
    CARS = 2
    REGISTERS = 3
    BRANDS = 4
    REPORTS = 5
