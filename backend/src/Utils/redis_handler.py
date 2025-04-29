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
            result = self._client.quit()

            if not result:
                raise ConnectionError("Não foi possível desconectar do redis")

            self._logger.debug("Client disconnected")
        except Exception as e:
            raise e

    def set_data(self, db: RedisDbsEnum, key: str, value: CacheDataType, ex: Optional[int] = None) -> Any:
        self._logger.info("Starting set_data")

        try:
            self._connect_client(db)

            client: Redis = self._client

            _value = json.dumps(jsonable_encoder(value))

            self._logger.debug(f"Setting key: {key} on db: {db} with ttl: {ex}")
            return client.set(key, _value, ex)
        except Exception as e:
            raise e
        finally:
            self._disconnect_client()

    def set_data_for_user(
        self,
        db: RedisDbsEnum,
        user_id: str,
        hash_key: str,
        value: CacheDataType,
        ex: int,
    ) -> Any:
        self._logger.info("Starting set_data")

        try:
            self._connect_client(db)

            client: Redis = self._client

            _value = json.dumps(jsonable_encoder(value))

            self._logger.debug(f"Setting key: {hash_key} on db: {db} with ttl: {ex}")
            result = client.hset(user_id, hash_key, _value)
            self._logger.debug("Data set")

            self._logger.debug("Setting TTL")
            client.expire(user_id, ex)
            self._logger.debug("TTL set")

            return result
        except Exception as e:
            raise e
        finally:
            self._disconnect_client()

    def get_data(self, db: RedisDbsEnum, key: str) -> CacheDataType:
        self._logger.info("Starting get_data")

        try:
            self._connect_client(db)

            client: Redis = self._client

            self._logger.debug(f"Searching for key: {key} on db: {db}")
            result: bytes | None = client.get(key)
            self._logger.debug(f"Data get {result}")

            return json.loads(result.decode()) if result else None
        except Exception as e:
            raise e
        finally:
            self._disconnect_client()

    def get_data_from_user(self, db: RedisDbsEnum, user_id: str, b64_key: str) -> CacheDataType:
        self._logger.info("Starting get_data")

        try:
            self._connect_client(db)

            client: Redis = self._client

            self._logger.debug(f"Searching for key: {b64_key} on db: {db}")
            result = client.hget(user_id, b64_key)
            self._logger.debug(f"Data get {result}")

            return json.loads(result.decode()) if result else None
        except Exception as e:
            raise e
        finally:
            self._disconnect_client()

    def delete_data(self, db: RedisDbsEnum, key: str) -> Any:
        self._logger.info("Starting delete_data")

        try:
            self._connect_client(db)

            client: Redis = self._client

            self._logger.debug(f"Deleting key: {key} on db: {db}")
            result = client.delete(key)
            self._logger.debug("Data deleted")
            return result

        except Exception as e:
            raise e
        finally:
            self._disconnect_client()
