import logging
from abc import ABC


class BaseRepository(ABC):
    __logger: logging.Logger | None = None

    @property
    def logger(self) -> logging.Logger:
        if self.__logger is None:
            raise Warning(f"Initialize the router first using self.router = self.create_router()")
        return self.__logger

    @logger.setter
    def logger(self, value: logging.Logger) -> None:
        if not isinstance(value, logging.Logger):
            raise TypeError("Logger must be an instance of logging.Logger")
        self.__logger = value

    def create_logger(self, name: str) -> None:
        self.logger = logging.getLogger(name)
