from enum import IntEnum


class RedisDbsEnum(IntEnum):
    """
    Redis databases enum.
    """

    USERS = 0
    TOKENS = 1
    VEHICLES = 2
    REGISTERS = 3
    BRANDS = 4
    REPORTS = 5
    SESSIONS = 6
    FUEL_TYPES = 7
    SYNC_INITIAL = 8
    SYNC_UPDATES = 9
