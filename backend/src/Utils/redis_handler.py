import json
import os
from typing import Any, Optional

from Enums import RedisDbsEnum
from fastapi.encoders import jsonable_encoder
from Interfaces.cache_handler import CacheHandler
from redis import Redis

from .custom_primitive_types import CacheDataType


class RedisHandler(CacheHandler):
    def __init__(self) -> None:
        self.create_logger(__name__)

    def _connect_client(self, db: RedisDbsEnum) -> None:
        self._logger.info("Starting create_redis_client")

        redis_host = os.getenv("REDIS_HOST")
        redis_user = os.getenv("REDIS_USER")
        redis_password = os.getenv("REDIS_PASSWORD")
        redis_port = os.getenv("REDIS_PORT")
        health_check_interval = int(os.getenv("REDIS_HEALTH_CHECK_INTERVAL", 60))

        try:
            client = Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                username=redis_user,
                db=db.value,
                health_check_interval=health_check_interval,
            )

            self._set_client(client)

        except Exception as e:
            raise e

    def _disconnect_client(self) -> None:
        self._logger.info("Starting disconnect_client")
        try:
            self._logger.debug("Disconnecting client")
            self._client.close()

        except Exception as e:
            raise e

    def set_data(self, db: RedisDbsEnum, key: str, value: CacheDataType, ex: Optional[int] = None) -> Any:
        self._logger.info("Starting set_data")

        _value = json.dumps(jsonable_encoder(value))

        self._logger.debug(f"Setting key: {key} on db: {db} with ttl: {ex}")
        return self._execute_redis_command(db, self._client.set, name=key, value=_value, ex=ex)

    def set_data_for_user(
        self,
        db: RedisDbsEnum,
        user_id: str,
        hash_key: str,
        value: CacheDataType,
        ex: int,
    ) -> Any:
        self._logger.info("Starting set_data")

        _value = json.dumps(jsonable_encoder(value))

        self._logger.debug(f"Setting key: {hash_key} on db: {db} with ttl: {ex}")
        self._execute_redis_command(db, self._client.hset, user_id, hash_key, value=_value)
        self._logger.debug("Data set")

        self._logger.debug("Setting TTL")
        self._execute_redis_command(db, self._client.expire, user_id, ex)
        self._logger.debug("TTL set")

    def get_data(self, db: RedisDbsEnum, key: str) -> CacheDataType:
        self._logger.info("Starting get_data")

        self._logger.debug(f"Searching for key: {key} on db: {db}")
        result = self._execute_redis_command(db, self._client.exists, key)
        self._logger.debug(f"Data get {result}")

        return json.loads(str(result)) if result else None

    def get_data_from_user(self, db: RedisDbsEnum, user_id: str, b64_key: str) -> CacheDataType:
        self._logger.info("Starting get_data")

        self._logger.debug(f"Searching for key: {b64_key} on db: {db}")

        result = self._execute_redis_command(db, self._client.hget, user_id, b64_key)
        self._logger.debug(f"Data get {result}")

        return json.loads(str(result)) if result else None

    def delete_data(self, db: RedisDbsEnum, key: str) -> Any:
        self._logger.info("Starting delete_data")

        self._logger.debug(f"Deleting key: {key} on db: {db}")

        result = self._execute_redis_command(db, self._client.delete, key)

        self._logger.debug("Data deleted")

        return result
