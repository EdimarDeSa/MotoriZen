import logging
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Any, Optional

from Utils.custom_primitive_types import CacheDataType


class CacheHandler(ABC):
    __logger: logging.Logger | None = None

    @property
    def _logger(self) -> logging.Logger:
        return self.__logger

    def create_logger(self, name: str) -> None:
        self.__logger = logging.getLogger(name)

    __client: object | None = None

    @property
    def _client(self) -> object:
        return self.__client

    def _set_client(self, client: object) -> None:
        self.__client = client

    @abstractmethod
    def _connect_client(self, db: IntEnum) -> None: ...

    @abstractmethod
    def _disconnect_client(self) -> None: ...

    @abstractmethod
    def set_data(self, db: IntEnum, key: str, value: CacheDataType, ex: Optional[int] = None) -> Any: ...

    @abstractmethod
    def set_data_for_user(
        self,
        db: IntEnum,
        user_id: str,
        hash_key: str,
        value: CacheDataType,
        ex: int,
    ) -> Any: ...

    @abstractmethod
    def get_data(self, db: IntEnum, key: str) -> CacheDataType: ...

    @abstractmethod
    def get_data_from_user(self, db: IntEnum, user_id: str, b64_key: str) -> CacheDataType: ...

    @abstractmethod
    def delete_data(self, db: IntEnum, key: str) -> Any: ...
