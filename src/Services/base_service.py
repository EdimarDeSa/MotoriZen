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

    def insert_user_cache_data(
        self,
        db: RedisDbsEnum,
        id_user: str,
        b64_hash: str,
        data_dict: dict[str, Any] | list[dict[str, Any]],
    ) -> None:
        """
        Insert data into cache for the given user.

        Args:
            db (RedisDbsEnum): Database from which to retrieve data.
            id_user (str): User ID for which to retrieve data.
            hash_key (str): Hash key for the user's data.
            data_dict (dict[str, Any] | list[dict[str, Any]]): Data to be cached.
        """
        self.logger.debug("Starting _cache_data")
        self.cache_handler.set_data_for_user(db, id_user, b64_hash, data_dict, int(os.getenv("REDIS_TTL", 300)))
        self.logger.debug("Data cached")

    def get_user_cached_data(
        self, db: RedisDbsEnum, id_user: str, b64_hash: str
    ) -> Union[dict[str, Any], list[Any], None] | None:
        """
        Retrieves data from cache for the given user.

        Args:
            db (RedisDbsEnum): Database from which to retrieve data.
            id_user (str): User ID for which to retrieve data.
            hash_key (str): Hash key for the user's data.

        Returns:
            Union[dict[str, Any], list[Any], None] | None: Data from cache if found, otherwise None.
        """
        self.logger.debug("Starting get_cached_data")

        schema: Any = self.cache_handler.get_data_from_user(db, id_user, b64_hash)

        self.logger.debug(f"Cached data: {None if not schema else 'found'}")

        return schema

    def create_hash_key(self, data: dict[str, Any]) -> str:
        """
        Creates a hash key for the data.

        Args:
            data (dict[str, Any]): Values to be hashed.

        Returns:
            str: Hash key for the data.
        """
        self.logger.debug("Starting create_hash")

        self.logger.debug("Creating hash")
        b64_hash = base64.b64encode(bytes(json.dumps(data), "utf-8")).decode("utf-8")

        self.logger.debug(f"Hash created")

        return b64_hash

    def reset_cache(self, id_user: str) -> None:
        """
        Resets cache for the given user.

        Args:
            db (RedisDbsEnum): Database from which to retrieve data.
            id_user (str): User ID for which to retrieve data.
        """
        self.logger.debug("Starting reset_cache")

        self.logger.debug("Resetting cache")

        dbs = [
            RedisDbsEnum.CARS,
            RedisDbsEnum.REGISTERS,
            RedisDbsEnum.REPORTS,
        ]
        for db in dbs:
            self.cache_handler.delete_data(db, id_user)

        self.logger.debug("Cache reset")

    def create_session(self, write: bool = False) -> scoped_session[Session]:
        return DBConnectionHandler.create_session(write=write)

    @classmethod
    def calculate_offset(cls, per_page: int | None, page: int | None) -> int:
        """
        Create offset for SQLAlchemy query pagination.

        Args:
            per_page (int | None): Number of results per page.
            page (int | None): Actual page number.

        Returns:
            int: Offset for SQLAlchemy query pagination.
        """
        if per_page is None:
            per_page = 10

        if page is None:
            page = 1

        return per_page * (page - 1)

    @classmethod
    def calculate_max_pages(cls, total_results: int, per_page: int) -> int:
        """
        Calculate the maximum number of pages based on the total number of results and the results per page.

        Args:
            total_results (int): Total number of results.
            per_page (int): Results per page.

        Returns:
            int: Maximum number of pages.
        """
        pages = total_results / per_page

        int_pages = int(pages)

        if pages.is_integer():
            return int_pages

        return int_pages + 1
