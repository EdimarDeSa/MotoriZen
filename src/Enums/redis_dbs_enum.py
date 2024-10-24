from enum import IntEnum


class RedisDbsEnum(IntEnum):
    """
    Redis databases
    """

    USERS = 0
    TOKENS = 1
    CARS = 2
    RESULTS = 3
