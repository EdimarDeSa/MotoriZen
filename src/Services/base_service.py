from __future__ import annotations

import base64
import json
import logging
import os
from abc import ABC
from email.mime import base
from typing import Any, Sequence, Union

from sqlalchemy.orm import Session, scoped_session

from DB.connection_handler import DBConnectionHandler
from DB.Schemas.base_schema import BaseSchema
from Enums.redis_dbs_enum import RedisDbsEnum
from Utils.redis_handler import RedisHandler


class BaseService(ABC):
    _logger: logging.Logger
    _cache_handler: RedisHandler

    @property
    def logger(self) -> logging.Logger:
        if hasattr(self, "_logger") is False:
            raise Warning(f"Logger not initialized. Call self.logger = self.create_logger(__name__)")
        return self._logger

    @logger.setter
    def logger(self, value: logging.Logger) -> None:
        if not isinstance(value, logging.Logger):
            raise TypeError("Logger must be an instance of logging.Logger")
        self._logger = value

    def create_logger(self, name: str) -> None:
        self.logger = logging.getLogger(name)

    @property
    def cache_handler(self) -> RedisHandler:
        if hasattr(self, "_cache_handler") is False:
            self._cache_handler = RedisHandler()
        return self._cache_handler

    @cache_handler.setter
    def cache_handler(self, value: RedisHandler) -> None:
        if not isinstance(value, RedisHandler):
            raise TypeError("Cache handler must be an instance of RedisHandler")
        self._cache_handler = value

    def insert_cache_data(
        self,
        db: RedisDbsEnum,
        id_user: str,
        b64_hash: str,
        data_dict: dict[str, Any] | list[dict[str, Any]],
    ) -> None:
        data = {b64_hash: data_dict}
        self.logger.debug("Starting _cache_data")
        self.cache_handler.set_data(db, id_user, data, int(os.getenv("REDIS_TTL", 300)))
        self.logger.debug("Data cached")

    def get_user_cached_data(
        self, db: RedisDbsEnum, id_user: str, base64_hash: str
    ) -> Union[dict[str, Any], list[Any], None] | None:
        self.logger.debug("Starting get_cached_data")

        schema: Any = self.cache_handler.get_data_from_user(db, id_user, base64_hash)

        self.logger.debug(f"Cached data: {None if not schema else 'found'}")

        return schema

    def create_hash(self, data: dict[str, Any]) -> str:
        self.logger.debug("Starting create_hash")

        self.logger.debug("Creating hash")
        b64_hash = base64.b64encode(bytes(json.dumps(data), "utf-8")).decode("utf-8")

        self.logger.debug(f"Hash created: {b64_hash}")

        return b64_hash

    def create_session(self, write: bool = False) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(write=write)

    @classmethod
    def calculate_offset(cls, per_page: int | None, page: int | None) -> int:
        if per_page is None:
            per_page = 10

        if page is None:
            page = 1

        return per_page * (page - 1)

    @classmethod
    def calculate_max_pages(cls, total_results: int, per_page: int) -> int:
        pages = total_results / per_page

        int_pages = int(pages)

        if pages.is_integer():
            return int_pages

        return int_pages + 1
