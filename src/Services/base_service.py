from __future__ import annotations

import logging
from abc import ABC

from sqlalchemy.orm import Session, scoped_session

from DB.connection_handler import DBConnectionHandler


class BaseService(ABC):
    _logger: logging.Logger | None = None

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            raise Warning(f"Logger not initialized. Call self.logger = self.create_logger(__name__)")
        return self._logger

    @logger.setter
    def logger(self, value: logging.Logger) -> None:
        if not isinstance(value, logging.Logger):
            raise TypeError("Logger must be an instance of logging.Logger")
        self._logger = value

    def create_logger(self, name: str) -> None:
        self.logger = logging.getLogger(name)

    def create_session(self, write: bool = False) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(write=write)
