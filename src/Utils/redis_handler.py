import json
import logging
import os
from typing import Any, Optional, Union

from fastapi.encoders import jsonable_encoder
from redis import Redis

from Enums.redis_dbs_enum import RedisDbsEnum


class RedisHandler:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def __create_redis_client(self, db: RedisDbsEnum) -> Redis:
        self._logger.info("Starting create_redis_client")
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")

        return Redis(
            host=redis_host,
            port=redis_port,
            db=db.value,
            decode_responses=True,
        )

    def set_data(self, db: RedisDbsEnum, key: str, value: dict[str, Any] | list[Any], ex: Optional[int] = None) -> Any:
        self._logger.info("Starting set_data")
        redis = self.__create_redis_client(db)

        _value = json.dumps(jsonable_encoder(value))

        self._logger.debug(f"Setting key: {key} on db: {db} with ttl: {ex}")
        result = redis.set(name=key, value=_value, ex=ex)
        self._logger.debug("Data set")

        redis.quit()
        return result

    def get_data(self, db: RedisDbsEnum, key: str) -> Union[dict[str, Any], list[Any], None]:
        self._logger.info("Starting get_data")
        redis = self.__create_redis_client(db)
        self._logger.debug(f"Searching for key: {key} on db: {db}")
        result = redis.get(key)
        self._logger.debug(f"Data get {result}")
        redis.quit()
        json_result = json.loads(str(result)) if result else None
        return json_result

    def delete_data(self, db: RedisDbsEnum, key: str) -> Any:
        self._logger.info("Starting delete_data")
        redis = self.__create_redis_client(db)
        self._logger.debug(f"Deleting key: {key} on db: {db}")
        result = redis.delete(key)
        self._logger.debug("Data deleted")
        redis.quit()
        return result
